import * as THREE from 'three';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Crear la escena
var scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB); // Color celeste claro

// Crear la cámara
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.z = 5
// Crear el renderizador
// Renderer
const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Cargar el modelo .obj
var objLoader = new OBJLoader();

objLoader.load(
    './models/escena_completa_ed.obj',
    function (object) {
        var scale = 10
        object.scale.set(scale, scale, scale); // Ajusta estos valores según sea necesario
        object.traverse(function (child) {
            if (child.isMesh) {
                // Asignar un nuevo material con el color deseado
                child.material = new THREE.MeshBasicMaterial({ color: 0x000000 });
            }
        });
        scene.add(object);

        var boxHelper = new THREE.BoxHelper(object, 0xffff00);
        scene.add(boxHelper);
        
        // // Crear una caja delimitadora vacía
        // var boundingBox = new THREE.Box3();

        // // Recorrer todos los hijos del objeto cargado
        // object.traverse(function (child) {
        //     if (child.isMesh) {
        //         // Asegúrate de que la geometría del hijo se haya calculado
        //         child.geometry.computeBoundingBox();

        //         // Actualizar la caja delimitadora para incluir la geometría del hijo
        //         boundingBox.union(child.geometry.boundingBox);
        //     }
        // });
        // console.log(scene)
        // // Ahora puedes usar boundingBox para ajustar la cámara
        // var center = boundingBox.getCenter(new THREE.Vector3());
        // var size = boundingBox.getSize(new THREE.Vector3());
        // var maxDim = Math.max(size.x, size.y, size.z);
        // var fov = camera.fov * (Math.PI / 180);
        // var cameraZ = Math.abs(maxDim / 4 * Math.tan(fov * 2));
        // cameraZ *= 2; // Ajustar según sea necesario
        // camera.position.set(center.x, center.y, cameraZ);
        // camera.lookAt(center);
    },
    function (xhr) {
        // Esta función se llama durante la carga
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    function (error) {
        // Esta función se llama si ocurre un error
        console.log('An error happened');
    }
);

// objLoader.load(
//     './models/escena_completa_ed.obj',
//     // 'js_showtime/assets/mi_escena.obj', // Ruta al archivo .obj
//     function (object) {
//         scene.add(object);
//         object.position.y = -1.5; // Ajustar la posición según sea necesario
//     },
//     function (xhr) {
//         console.log((xhr.loaded / xhr.total * 100) + '% loaded');
//     },
//     function (error) {
//         console.log('An error happened');
//     }
// );

// // Función de animación
// function animate() {
//     requestAnimationFrame(animate);

//     // Aquí puedes añadir cualquier animación o rotación al objeto cargado si lo deseas

renderer.render(scene, camera);
// }
console.log('Deberia aparecer algo')
// animate();

// Ajustar la escena cuando se redimensiona la ventana
window.addEventListener('resize', function () {
    var width = window.innerWidth;
    var height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});
