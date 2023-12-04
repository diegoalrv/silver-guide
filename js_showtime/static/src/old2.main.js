import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Inicializar escena, cámara y renderer
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff); // 0xffffff es el código de color hexadecimal para blanco
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('myCanvas') });
renderer.setSize(window.innerWidth, window.innerHeight);
const controls = new OrbitControls(camera, renderer.domElement);
document.body.appendChild(renderer.domElement);

// Crear plano con textura de pasto
const loader = new THREE.TextureLoader();
const grassTexture = loader.load('/assets/textures/pasto.jpg');
const planeGeometry = new THREE.PlaneGeometry(10, 10);
const planeMaterial = new THREE.MeshBasicMaterial({ map: grassTexture });
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.position.y = 0;
scene.add(plane);

// Crear cajas rectangulares
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
    box.scale.y = height;
    box.position.set(Math.random() * 8 - 4, height / 2, Math.random() * 8 - 4);
    boxes.push(box);
    scene.add(box);
}

// Seleccionar una caja para moverla
const boxToMove = boxes[0]; // Por ejemplo, mover la primera caja

// Función para manejar el movimiento de la caja
function moveBox(event) {
    const key = event.key;
    const moveStep = 0.1;

    switch (key) {
      case 'ArrowUp':
        case 'w':
            boxToMove.position.z -= moveStep;
            break;
        case 'ArrowDown':
        case 's':
            boxToMove.position.z += moveStep;
            break;
        case 'ArrowLeft':
        case 'a':
            boxToMove.position.x -= moveStep;
            break;
        case 'ArrowRight':
        case 'd':
            boxToMove.position.x += moveStep;
            break;
        case 'i':
            boxToMove.position.y += moveStep;
            break;
        case 'o':
            boxToMove.position.y -= moveStep;
            break;
    }
}
// Agregar listener para eventos de teclado
document.addEventListener('keydown', moveBox);

// Configurar la cámara en una vista isométrica
const distancia = 10;
camera.position.set(0, distancia, distancia);
camera.lookAt(new THREE.Vector3(0, 0, 0));

// Variables para el movimiento orbital
let angle = Math.PI/4;
const radius = Math.sqrt(2)*distancia;

// Función de animación
function animate() {
    requestAnimationFrame(animate);


    // Actualizar posición de la cámara para la órbita
    // camera.position.x = radius * Math.cos(angle);
    // camera.position.z = radius * Math.sin(angle);
    // camera.position.y = radius * Math.sin(Math.PI / 4);
    camera.lookAt(new THREE.Vector3(0, 0, 0));

    // Incrementar el ángulo para la próxima frame
    angle += 0.01;

    renderer.render(scene, camera);
}

animate();
