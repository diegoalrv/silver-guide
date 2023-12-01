import * as THREE from 'three';
import modelUrl from './assets/Ceramic_pot_model.glb'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('myCanvas') });
const controls = new OrbitControls(camera, renderer.domElement);

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // color y intensidad
scene.add(ambientLight);

// const loader = new GLTFLoader();
// loader.load(modelUrl, function (gltf) {
//   scene.add(gltf.scene);
// }, undefined, function (error) {
//   console.error(error);
// });

// Crear la geometría del cubo
const geometry = new THREE.BoxGeometry(1, 1, 1); // dimensiones del cubo: ancho, alto, profundidad

// Crear el material del cubo
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 }); // color verde

// Crear el mesh (geometría + material)
const cube = new THREE.Mesh(geometry, material);

// Añadir el cubo a la escena
scene.add(cube);

camera.position.z = 1;

function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}

animate();
