import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff); // 0xffffff es el código de color hexadecimal para blanco

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('myCanvas') });
const controls = new OrbitControls(camera, renderer.domElement);

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // color y intensidad
scene.add(ambientLight);
const greenMaterial = new THREE.MeshStandardMaterial({ color: 0x00ff00 }); // Un color verde

const loader = new OBJLoader();
loader.load('/static/assets/tu_escena.obj', function (object) {
  object.traverse(function (child) {
    if (child.isMesh) {
        child.material = greenMaterial;
    }
  });
  scene.add(object);
}, undefined, function (error) {
    console.error(error);
});

// // Crear la geometría del cubo
// const geometry = new THREE.BoxGeometry(1, 1, 1); // dimensiones del cubo: ancho, alto, profundidad

// // Crear el material del cubo
// const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 }); // color verde

// // Crear el mesh (geometría + material)
// const cube = new THREE.Mesh(geometry, material);

// Añadir el cubo a la escena
// scene.add(cube);

camera.position.z = 10;

function animate() {
  requestAnimationFrame(animate);
  // cube.rotation.x += 0.01;
  // cube.rotation.y += 0.01;
  controls.update();
  renderer.render(scene, camera);
}

animate();
