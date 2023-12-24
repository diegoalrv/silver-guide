import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Inicializar escena, cámara y renderer
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff); // Color blanco
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('myCanvas') });
renderer.setSize(window.innerWidth, window.innerHeight);
const controls = new OrbitControls(camera, renderer.domElement);
document.body.appendChild(renderer.domElement);

// Crear plano en el eje XY
const loader = new THREE.TextureLoader();
const grassTexture = loader.load('/src/assets/textures/pasto.jpg');
const planeGeometry = new THREE.PlaneGeometry(15, 15);
const planeMaterial = new THREE.MeshBasicMaterial({ map: grassTexture });
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
scene.add(plane);

// Crear cajas con base en el plano XY y elevación en el eje Z
const boxGeometry = new THREE.BoxGeometry(1, 1, 1);
const boxMaterials = [
    new THREE.MeshBasicMaterial({ color: 0xff0000 }),
    new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
    new THREE.MeshBasicMaterial({ color: 0x0000ff })
];
const boxes = [];
for (let i = 0; i < 3; i++) {
    const box = new THREE.Mesh(boxGeometry, boxMaterials[i]);
    const height = Math.random() * 3 + 1;
    box.scale.z = height;
    box.position.set(Math.random() * 8 - 4, Math.random() * 8 - 4, height / 2);
    boxes.push(box);
    scene.add(box);
}

// Configurar la cámara en una vista isométrica
const distancia = 10;
camera.position.set(distancia, distancia, distancia);
camera.lookAt(new THREE.Vector3(0, 0, 0));

// Crear un indicador de ejes
const axesHelper = new THREE.AxesHelper(5); // El número (5) es la longitud de cada eje
scene.add(axesHelper);

// Función de animación
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

animate();
