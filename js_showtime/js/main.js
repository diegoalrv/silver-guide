// Configuración básica de la escena
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Cargar la textura
const textureLoader = new THREE.TextureLoader();
const texture = textureLoader.load('assets/textures/manzanas.png');

// Cargar el modelo OBJ
const objLoader = new THREE.OBJLoader();
objLoader.load(
    '../assets/models/escena_completa_ed.obj',
    (object) => {
        // Aplicar la textura al modelo
        object.traverse((child) => {
            if (child instanceof THREE.Mesh) {
                child.material.map = texture;
            }
        });
        scene.add(object);
    },
    (xhr) => {
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    (error) => {
        console.log('An error happened');
    }
);

camera.position.z = 5;

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

animate();
