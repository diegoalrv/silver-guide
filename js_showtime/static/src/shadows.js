import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Crear la escena y la cámara
var scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);  // Fondo blanco

var camera = new THREE.OrthographicCamera(window.innerWidth / -2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / -2, 1, 1000);
camera.position.set(200, 200, 200);
camera.lookAt(scene.position);

// Crear el renderizador
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('myCanvas') });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Mejor renderizado de sombras
const controls = new OrbitControls(camera, renderer.domElement);
document.body.appendChild(renderer.domElement);


// Crear una luz direccional (Simula el sol)
var sunLight = new THREE.DirectionalLight(0xffffff, 1);
sunLight.position.set(100, 100, 100);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;  // Mayor resolución de sombras
sunLight.shadow.mapSize.height = 2048;
var d = 100;
sunLight.shadow.camera.left = -d;
sunLight.shadow.camera.right = d;
sunLight.shadow.camera.top = d;
sunLight.shadow.camera.bottom = -d;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 500;
scene.add(sunLight);

// Crear una esfera para representar el sol
var sunGeometry = new THREE.SphereGeometry(5, 32, 32);
var sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });  // Material amarillo para el sol
var sunMesh = new THREE.Mesh(sunGeometry, sunMaterial);
scene.add(sunMesh);

// Función para crear edificios
function createBuilding(x, y, z, width, height, depth) {
    var geometry = new THREE.BoxGeometry(width, height, depth);
    var material = new THREE.MeshStandardMaterial({ color: 0x808080 });
    var building = new THREE.Mesh(geometry, material);
    building.position.set(x, y, z);
    building.castShadow = true;
    building.receiveShadow = true;
    scene.add(building);
}

// Crear dos edificios
createBuilding(-30, 20, -10, 20, 40, 20);
createBuilding(30, 15, 20, 20, 30, 20);

// Función para crear casas
function createHouse(x, y, z, width, height, depth) {
    var geometry = new THREE.BoxGeometry(width, height, depth);
    var material = new THREE.MeshStandardMaterial({ color: 0xa0522d });
    var house = new THREE.Mesh(geometry, material);
    house.position.set(x, y, z);
    house.castShadow = true;
    house.receiveShadow = true;
    scene.add(house);
}

// Crear tres casas
createHouse(-60, 10, 40, 20, 20, 20);
createHouse(-20, 10, 60, 20, 20, 20);
createHouse(60, 10, -40, 20, 20, 20);

// Crear una calle
var streetGeometry = new THREE.PlaneGeometry(200, 10);
var streetMaterial = new THREE.MeshStandardMaterial({ color: 0x333333, side: THREE.DoubleSide });
var street = new THREE.Mesh(streetGeometry, streetMaterial);
street.rotation.x = -Math.PI / 2;
street.position.y = 0;
street.receiveShadow = true;
scene.add(street);

// Crear un plano base
var planeGeometry = new THREE.PlaneGeometry(300, 300);
var planeMaterial = new THREE.MeshStandardMaterial({ color: 0xaaaaaa, side: THREE.DoubleSide });
var plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.position.y = -1;
plane.receiveShadow = true;  // Habilitar que este plano reciba sombras
scene.add(plane);

// Animación y simulación del movimiento del sol
var dayTime = 0;  // Variable para simular el tiempo del día

function animate() {
    requestAnimationFrame(animate);

    // Simular el movimiento del sol a lo largo del día
    dayTime += 0.005;
    var x = 200 * Math.sin(dayTime);
    var y = 200 * Math.abs(Math.cos(dayTime));
    var z = 200 * Math.cos(dayTime);
    sunLight.position.set(x, y, z);
    sunMesh.position.set(x, y, z);  // Actualizar la posición de la esfera del sol

    renderer.render(scene, camera);
}

animate();

animate();
