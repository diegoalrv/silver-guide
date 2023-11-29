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

// Crear el cubo
var geometry = new THREE.BoxGeometry();
var material = new THREE.MeshBasicMaterial({ color: 0xFF8C00 }); // Naranja oscuro
var cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Crear el plano (pasto)
var planeGeometry = new THREE.PlaneGeometry(10, 10);
var planeMaterial = new THREE.MeshBasicMaterial({ color: 0x008000, side: THREE.DoubleSide }); // Verde
var plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.position.y = -1.5;
scene.add(plane);

// Añadir bordes al cubo
var edges = new THREE.EdgesGeometry(geometry);
var line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x000000 })); // Negro
cube.add(line);

// Función de animación
function animate() {
    requestAnimationFrame(animate);

    // Rotar el cubo
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

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
