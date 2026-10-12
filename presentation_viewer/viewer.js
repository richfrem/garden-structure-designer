/**
 * viewer.js
 * =========
 *
 * Purpose:
 *     Three.js presentation viewer for the authoritative solid assembly. Loads a member-indexed
 *     GLB, renders it with opaque depth-tested Yellow Cedar materials, a 45-degree-style sun with
 *     soft shadows and a grade shadow plane, verifies >= 24 depth bits, and publishes
 *     `window.renderStatus` (loading | ready | error) for the Playwright capture harness.
 *     Hardware-style depth testing replaces any Painter's-algorithm ordering.
 *
 * Key Input Dependencies:
 *     - ./vendor/three.module.js, ./vendor/GLTFLoader.js, ./utils/BufferGeometryUtils.js (pinned local copies, no CDN)
 *     - ./model.glb and ./model.glb.manifest.json (written by cad_export_glb.py; served by render_presentation_webgl.py)
 *     - URL query params: glb, manifest, camera (isometric | perspective)
 *
 * Usage Examples:
 *     Served via loopback by render_presentation_webgl.py:
 *     http://127.0.0.1:<port>/viewer.html?glb=./model.glb&manifest=./model.glb.manifest.json&camera=isometric
 *
 * Key Functions:
 *     createRenderer(container, width, height) -> THREE.WebGLRenderer
 *     assertDepthBits(renderer) -> number
 *     computeFraming(bounds) -> {center, span}
 *     createCamera(cameraType, framing, width, height) -> THREE.Camera
 *     addLighting(scene, framing) -> void
 *     addGroundPlane(scene, framing, bounds) -> void
 *     createMaterials() -> {wood, footing}
 *     loadAssembly(glbUrl, scene, materials) -> Promise<void>
 *     initViewer() -> Promise<void>
 */
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/GLTFLoader.js';

const MIN_DEPTH_BITS = 24;

window.renderStatus = {
  state: 'loading', // loading | ready | error
  requestId: null,
  revisionHash: null,
  assemblyHash: null,
  cameraHash: null,
  depthBits: null,
  memberIds: [],
  viewport: null,
  error: null,
};

/**
 * Creates the WebGL renderer with shadows and appends its canvas to the container.
 * @param {HTMLElement} container Element receiving the canvas.
 * @param {number} width Viewport width in pixels.
 * @param {number} height Viewport height in pixels.
 * @returns {THREE.WebGLRenderer} Configured renderer.
 */
function createRenderer(container, width, height) {
  const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance',
  });
  renderer.setSize(width, height);
  renderer.setPixelRatio(1.0);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  container.appendChild(renderer.domElement);
  return renderer;
}

/**
 * Reads the depth buffer precision and fails when below the required minimum.
 * @param {THREE.WebGLRenderer} renderer Active renderer.
 * @returns {number} Depth bits reported by the context.
 */
function assertDepthBits(renderer) {
  const gl = renderer.getContext();
  const depthBits = gl.getParameter(gl.DEPTH_BITS);
  window.renderStatus.depthBits = depthBits;
  if (depthBits < MIN_DEPTH_BITS) {
    throw new Error(`Insufficient WebGL depth precision: ${depthBits} bits (requires >= ${MIN_DEPTH_BITS})`);
  }
  return depthBits;
}

/**
 * Derives the assembly center and largest span from manifest bounds (millimetres).
 * @param {number[][]} bounds [[minX, minY, minZ], [maxX, maxY, maxZ]].
 * @returns {{center: number[], span: number}} Framing data.
 */
function computeFraming(bounds) {
  const center = [0, 1, 2].map((i) => (bounds[0][i] + bounds[1][i]) / 2.0);
  const span = Math.max(...[0, 1, 2].map((i) => bounds[1][i] - bounds[0][i]));
  return { center, span };
}

/**
 * Builds a perspective, isometric, plan, or elevation camera looking at the assembly center.
 * Aligned 1:1 with CAD coordinate system (+Z up).
 * @param {string} cameraType 'perspective', 'isometric', 'plan', or 'elevation'.
 * @param {{center: number[], span: number}} framing Assembly framing.
 * @param {number} width Viewport width.
 * @param {number} height Viewport height.
 * @returns {THREE.Camera} Positioned camera.
 */
function createCamera(cameraType, framing, width, height) {
  const { center, span } = framing;
  // Match sheet_composer.py margins (100px total) and scale formula:
  // scale = min(w - 100, h - 100) / (span * 1.5)
  const viewW = Math.max(10, width - 100);
  const viewH = Math.max(10, height - 100);
  const scale = Math.min(viewW, viewH) / (span * 1.5);
  const frustumWidth = width / scale;
  const frustumHeight = height / scale;
  let camera;

  if (cameraType === 'plan') {
    // Top-down: looking from +Z down to -Z. Right is +X, Up is +Y.
    camera = new THREE.OrthographicCamera(
      -frustumWidth / 2, frustumWidth / 2,
      frustumHeight / 2, -frustumHeight / 2,
      10, 50000,
    );
    camera.position.set(center[0], center[1], center[2] + span * 2.0);
    camera.up.set(0, 1, 0);
  } else if (cameraType === 'elevation' || cameraType === 'front_elevation') {
    // Front elevation: looking from -Y toward +Y. Right is +X, Up is +Z.
    camera = new THREE.OrthographicCamera(
      -frustumWidth / 2, frustumWidth / 2,
      frustumHeight / 2, -frustumHeight / 2,
      10, 50000,
    );
    camera.position.set(center[0], center[1] - span * 2.0, center[2]);
    camera.up.set(0, 0, 1);
  } else if (cameraType === 'perspective') {
    // True perspective looking toward assembly center.
    // 50 deg vertical FOV matches cad_camera create_perspective_camera fov_y_deg=50
    camera = new THREE.PerspectiveCamera(50, width / height, 10, 50000);
    camera.position.set(center[0] + span * 1.5, center[1] - span * 1.8, center[2] + span * 1.2);
    camera.up.set(0, 0, 1);
  } else {
    // Default Isometric: CAD outward (1, -1, 1)/sqrt(3), Up (-1, 1, 2)/sqrt(6)
    camera = new THREE.OrthographicCamera(
      -frustumWidth / 2, frustumWidth / 2,
      frustumHeight / 2, -frustumHeight / 2,
      10, 50000,
    );
    const dist = (span * 2.0) / Math.sqrt(3);
    camera.position.set(center[0] + dist, center[1] - dist, center[2] + dist);
    camera.up.set(-1 / Math.sqrt(6), 1 / Math.sqrt(6), 2 / Math.sqrt(6));
  }

  camera.lookAt(center[0], center[1], center[2]);
  return camera;
}

/**
 * Adds ambient fill and a shadow-casting directional sun fitted to the assembly span.
 * @param {THREE.Scene} scene Target scene.
 * @param {{center: number[], span: number}} framing Assembly framing.
 * @returns {void}
 */
function addLighting(scene, framing) {
  const { center, span } = framing;
  scene.add(new THREE.AmbientLight(0xffffff, 0.65));
  const sun = new THREE.DirectionalLight(0xfff8ee, 1.2);
  sun.position.set(center[0] + span * 1.5, center[1] - span * 1.5, center[2] + span * 2.0);
  sun.castShadow = true;
  sun.shadow.mapSize.set(4096, 4096);
  sun.shadow.camera.near = 10;
  sun.shadow.camera.far = span * 5.0;
  const extent = span * 1.2;
  Object.assign(sun.shadow.camera, { left: -extent, right: extent, top: extent, bottom: -extent });
  sun.shadow.bias = -0.0001;
  scene.add(sun);
}

/**
 * Adds a shadow-receiving grade plane just below the assembly.
 * @param {THREE.Scene} scene Target scene.
 * @param {{center: number[], span: number}} framing Assembly framing.
 * @param {number[][]} bounds Assembly bounds in millimetres.
 * @returns {void}
 */
function addGroundPlane(scene, framing, bounds, cameraType) {
  // Do not cast grade shadows in top-down plan view to keep framing diagram clean
  if (cameraType === 'plan') return;
  const { center, span } = framing;
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(span * 5, span * 5),
    new THREE.ShadowMaterial({ opacity: 0.25 }),
  );
  ground.position.set(center[0], center[1], bounds[0][2] - 10);
  ground.receiveShadow = true;
  scene.add(ground);
}

/**
 * Creates the opaque, depth-tested materials used for timber and footings.
 * @returns {{wood: THREE.MeshStandardMaterial, footing: THREE.MeshStandardMaterial}} Materials.
 */
function createMaterials() {
  const base = { metalness: 0.0, depthTest: true, depthWrite: true };
  return {
    wood: new THREE.MeshStandardMaterial({ color: 0xddb892, roughness: 0.82, ...base }),
    footing: new THREE.MeshStandardMaterial({ color: 0x888888, roughness: 0.95, ...base }),
  };
}

/**
 * Loads the GLB, applies member materials, and resolves once the model is in the scene.
 * @param {string} glbUrl GLB location.
 * @param {THREE.Scene} scene Target scene.
 * @param {{wood: THREE.Material, footing: THREE.Material}} materials Material set.
 * @returns {Promise<void>} Resolves on load, rejects on loader error.
 */
function loadAssembly(glbUrl, scene, materials) {
  return new Promise((resolve, reject) => {
    new GLTFLoader().load(glbUrl, (gltf) => {
      gltf.scene.traverse((node) => {
        if (!node.isMesh) return;
        node.castShadow = true;
        node.receiveShadow = true;
        node.material = (node.name || '').startsWith('FT') ? materials.footing : materials.wood;
      });
      scene.add(gltf.scene);
      resolve();
    }, undefined, reject);
  });
}

/**
 * Entry point: loads the manifest, builds the scene, renders two frames, and marks the viewer ready.
 * Any failure sets renderStatus.state to 'error' with the message.
 * @returns {Promise<void>} Resolves when rendering settles.
 */
async function initViewer() {
  try {
    const params = new URLSearchParams(window.location.search);
    const manifestResp = await fetch(params.get('manifest') || './model.glb.manifest.json');
    if (!manifestResp.ok) throw new Error(`Manifest load failed: HTTP ${manifestResp.status}`);
    const manifest = await manifestResp.json();
    window.renderStatus.assemblyHash = manifest.assembly_sha256;
    window.renderStatus.memberIds = manifest.members.map((m) => m.member_id);

    const width = window.innerWidth;
    const height = window.innerHeight;
    window.renderStatus.viewport = { width, height };
    const renderer = createRenderer(document.getElementById('canvas-container'), width, height);
    assertDepthBits(renderer);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);
    const framing = computeFraming(manifest.bounds_mm);
    const cameraType = params.get('camera') || 'isometric';
    const camera = createCamera(cameraType, framing, width, height);
    addLighting(scene, framing);
    addGroundPlane(scene, framing, manifest.bounds_mm, cameraType);
    await loadAssembly(params.get('glb') || './model.glb', scene, createMaterials());

    renderer.render(scene, camera);
    requestAnimationFrame(() => {
      renderer.render(scene, camera);
      window.renderStatus.state = 'ready';
    });
  } catch (err) {
    window.renderStatus.state = 'error';
    window.renderStatus.error = (err && err.message) || String(err);
  }
}

window.addEventListener('DOMContentLoaded', initViewer);
