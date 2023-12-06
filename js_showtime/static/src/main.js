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
const boxToMove = boxes[0];

// Verificar si hay un nuevo movimiento
function checkForNewMovement() {
    fetch('http://localhost:5000/is_new_movement')
        .then(response => response.json())
        .then(data => {
            if (data.state) {
                fetchMovementDetails();
            }
        })
        .catch(error => console.error('Error al verificar nuevo movimiento:', error));
}

// Obtener detalles del movimiento
function fetchMovementDetails() {
    fetch('http://localhost:5000/get_movement')
        .then(response => response.json())
        .then(data => {
            applyMovement(data);
            moveApplied(); // Notificar que el movimiento ha sido aplicado
        })
        .catch(error => console.error('Error al obtener detalles de movimiento:', error));
}

// Aplicar el movimiento a la caja
function applyMovement(data) {
  const moveStep = data.steps * 0.1; // Este es el cambio total deseado
  const targetPosition = new THREE.Vector3(
      boxToMove.position.x + (data.axis === 'x' ? moveStep : 0),
      boxToMove.position.y + (data.axis === 'y' ? moveStep : 0),
      boxToMove.position.z + (data.axis === 'z' ? moveStep : 0)
  );

  const speed = data.speed; // Esto determinará qué tan rápido se hace el cambio

  // Calcular la cantidad de frames necesarios para el movimiento, basado en la velocidad
  const frames = Math.abs(moveStep / speed);

  // Crear una función que se ejecute en cada frame para mover el objeto
  let currentFrame = 0;
  function moveObject() {
      if (currentFrame < frames) {
          boxToMove.position.lerp(targetPosition, currentFrame / frames);
          currentFrame++;
          setTimeout(() => {
            requestAnimationFrame(moveObject);
          }, 1000); // Pausa de 50 milisegundos
      } else {
          // Movimiento completado, puedes llamar a moveApplied aquí si es necesario
          boxToMove.position.set(targetPosition.x, targetPosition.y, targetPosition.z);
          // moveApplied(); // Notificar al backend que el movimiento ha sido aplicado
      }
  }

  // Iniciar el movimiento
  moveObject();
}

// Notificar al backend que el movimiento ha sido aplicado
function moveApplied() {
    fetch('http://localhost:5000/move_applied', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log('Movimiento aplicado:', data))
        .catch(error => console.error('Error al notificar movimiento aplicado:', error));
}

// Llamar a la función regularmente, por ejemplo, cada segundo
setInterval(checkForNewMovement, 10);

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
    renderer.render(scene, camera);
}

animate();
