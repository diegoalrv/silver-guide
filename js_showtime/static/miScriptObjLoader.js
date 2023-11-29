import * as THREE from 'three';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';

// Crear la escena
var scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB); // Color celeste claro

// Crear la cámara
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// Crear el renderizador
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Cargar el modelo .obj
var objLoader = new OBJLoader();
objLoader.load(
    'js_showtime/assets/models/escena_completa_ed.obj',
    // 'js_showtime/assets/mi_escena.obj', // Ruta al archivo .obj
    function (object) {
        scene.add(object);
        object.position.y = -1.5; // Ajustar la posición según sea necesario
    },
    function (xhr) {
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    function (error) {
        console.log('An error happened');
    }
);

// Función de animación
function animate() {
    requestAnimationFrame(animate);

    // Aquí puedes añadir cualquier animación o rotación al objeto cargado si lo deseas

    renderer.render(scene, camera);
}

animate();

// Ajustar la escena cuando se redimensiona la ventana
window.addEventListener('resize', function () {
    var width = window.innerWidth;
    var height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});
