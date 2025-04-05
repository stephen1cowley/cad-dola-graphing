// Add immediate logging
console.log('Script loaded');

let scene, camera, renderer;
let data = [];
let currentQuestion = null;
let points = [];
let simplex = null;
let axes = null;
let alphaLabels = []; // Track alpha labels
let connectingLines = []; // Track connecting lines
let labelUpdateFunctions = []; // Track label update functions

// Initialize Three.js scene
function init() {
    console.log('Initializing scene');
    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    // Create camera
    const aspect = (window.innerWidth - 300) / window.innerHeight;
    const frustumSize = 1.5; // Controls the size of the view
    camera = new THREE.OrthographicCamera(
        -frustumSize * aspect / 2,
        frustumSize * aspect / 2,
        frustumSize / 2,
        -frustumSize / 2,
        0.1,
        1000
    );
    camera.position.set(1.0, 1.0, 1.0);
    camera.lookAt(0, 0.35, 0);

    // Create renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth - 300, window.innerHeight);
    document.getElementById('container').appendChild(renderer.domElement);

    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Load data
    console.log('Fetching data...');
    fetch('all_distributions_memotrap/final_data_all_distributions.json', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            console.log('Response received:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(jsonData => {
            console.log('Data loaded successfully');
            console.log('Number of questions:', jsonData.length);
            if (jsonData.length === 0) {
                throw new Error('No questions found in data');
            }
            data = jsonData;
            populateQuestionSelect();
            createSimplex();
            createAxes();
            updateQuestion(0);
        })
        .catch(error => {
            console.error('Error loading data:', error);
            document.getElementById('question-select').innerHTML = `<option value="">Error loading data: ${error.message}</option>`;
        });

    // Handle window resize
    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    camera.aspect = (window.innerWidth - 300) / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth - 300, window.innerHeight);
}

function createSimplex() {
    // Create the triangular simplex
    const geometry = new THREE.BufferGeometry();
    const vertices = new Float32Array([
        1, 0, 0,  // first key
        0, 1, 0,  // second key
        0, 0, 1   // third key
    ]);
    geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    
    const material = new THREE.MeshBasicMaterial({ 
        color: 0x808080,
        transparent: true,
        opacity: 0.3,
        side: THREE.DoubleSide
    });
    
    // Create a mesh for the simplex
    simplex = new THREE.Mesh(geometry, material);
    scene.add(simplex);
}

function createAxes() {
    // Create custom axes with gray color
    const axesMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
    
    // Create cylinders for each axis
    const radius = 0.002; // Thickness of the axes
    const height = 1.05;  // Length of the axes
    
    // X-axis cylinder
    const xGeometry = new THREE.CylinderGeometry(radius, radius, height, 8);
    const xAxis = new THREE.Mesh(xGeometry, axesMaterial);
    xAxis.rotation.z = Math.PI / 2; // Rotate to align with x-axis
    xAxis.position.set(height/2, 0, 0);
    scene.add(xAxis);
    
    // Y-axis cylinder
    const yGeometry = new THREE.CylinderGeometry(radius, radius, height, 8);
    const yAxis = new THREE.Mesh(yGeometry, axesMaterial);
    yAxis.position.set(0, height/2, 0);
    scene.add(yAxis);
    
    // Z-axis cylinder
    const zGeometry = new THREE.CylinderGeometry(radius, radius, height, 8);
    const zAxis = new THREE.Mesh(zGeometry, axesMaterial);
    zAxis.rotation.x = Math.PI / 2; // Rotate to align with z-axis
    zAxis.position.set(0, 0, height/2);
    scene.add(zAxis);

    // Create arrowheads for each axis
    const arrowMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
    const arrowGeometry = new THREE.ConeGeometry(0.008, 0.05, 50);

    // X-axis arrow
    const xArrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
    xArrow.position.set(1.05, 0, 0);
    xArrow.rotation.z = -Math.PI / 2;
    scene.add(xArrow);

    // Y-axis arrow
    const yArrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
    yArrow.position.set(0, 1.05, 0);
    scene.add(yArrow);

    // Z-axis arrow
    const zArrow = new THREE.Mesh(arrowGeometry, arrowMaterial);
    zArrow.position.set(0, 0, 1.05);
    zArrow.rotation.x = Math.PI / 2;
    scene.add(zArrow);
}

function createPoints(distributions) {
    console.log('createPoints called with distributions:', distributions);
    
    // Remove existing points, lines, and labels
    console.log('Removing existing points:', points.length);
    points.forEach(point => scene.remove(point));
    points = [];
    
    // Remove existing lines
    connectingLines.forEach(line => scene.remove(line));
    connectingLines = [];
    
    // Remove existing alpha labels and their update functions
    alphaLabels.forEach(label => {
        document.body.removeChild(label);
    });
    alphaLabels = [];
    
    // Remove resize event listeners for old labels
    labelUpdateFunctions.forEach(func => {
        window.removeEventListener('resize', func);
    });
    labelUpdateFunctions = [];

    // Create points for each distribution
    const geometry = new THREE.SphereGeometry(0.02, 16, 16);
    const material = new THREE.MeshBasicMaterial({ color: 0x00b400 }); // Changed to green

    // Convert object to array of distributions
    const distributionArray = Object.entries(distributions).map(([key, value]) => ({
        ...value,
        position: parseFloat(key)
    }));

    // Sort by position
    distributionArray.sort((a, b) => a.position - b.position);

    // Create a line material
    const lineMaterial = new THREE.MeshBasicMaterial({ color: 0x00b400 });
    const lineRadius = 0.005; // Thickness of the connecting lines

    distributionArray.forEach((dist, index) => {
        console.log('Processing distribution', index, ':', dist);
        if (!dist) {
            console.error('Invalid distribution at index', index);
            return;
        }
        
        // Get the three keys from the distribution
        const keys = Object.keys(dist).filter(k => k !== 'position');
        if (keys.length !== 3) {
            console.error('Distribution should have exactly 3 keys, found:', keys.length);
            return;
        }

        // Check if all values are numbers
        const values = keys.map(key => dist[key]);
        if (!values.every(val => typeof val === 'number')) {
            console.error('Not all values are numbers in distribution', index, ':', dist);
            return;
        }

        const point = new THREE.Mesh(geometry, material);
        point.position.set(
            dist[keys[0]],
            dist[keys[1]],
            dist[keys[2]]
        );
        scene.add(point);
        points.push(point);

        // Add connecting cylinder if this isn't the first point
        if (index > 0) {
            const prevPoint = points[index - 1];
            const start = prevPoint.position;
            const end = point.position;
            
            // Calculate the midpoint and length
            const midpoint = new THREE.Vector3().addVectors(start, end).multiplyScalar(0.5);
            const length = start.distanceTo(end);
            
            // Create cylinder
            const cylinderGeometry = new THREE.CylinderGeometry(lineRadius, lineRadius, length, 8);
            const cylinder = new THREE.Mesh(cylinderGeometry, lineMaterial);
            
            // Position the cylinder at the midpoint
            cylinder.position.copy(midpoint);
            
            // Create a direction vector and calculate the rotation
            const direction = new THREE.Vector3().subVectors(end, start).normalize();
            cylinder.lookAt(end);
            cylinder.rotateX(Math.PI / 2); // Rotate to align with the direction
            
            scene.add(cylinder);
            connectingLines.push(cylinder);
        }

        // Add alpha label if position is between -1.0 and 1.5 or 4.0
        if (dist.position >= -1.0 && dist.position <= 1.5 || dist.position == 4.0) {
            const labelDiv = document.createElement('div');
            labelDiv.className = 'alpha-label';
            labelDiv.textContent = `α=${dist.position.toFixed(1)}`;
            labelDiv.style.position = 'absolute';
            labelDiv.style.color = 'black';
            labelDiv.style.fontSize = '32px';
            document.body.appendChild(labelDiv);
            alphaLabels.push(labelDiv);

            function updateLabelPosition() {
                const xOffset = parseFloat(document.getElementById('label-x-offset').value) || 0;
                const yOffset = parseFloat(document.getElementById('label-y-offset').value) || 0.05;
                const zOffset = parseFloat(document.getElementById('label-z-offset').value) || 0;

                const xRotation = (parseFloat(document.getElementById('label-x-rotation').value) || 0) * Math.PI / 180;
                const yRotation = (parseFloat(document.getElementById('label-y-rotation').value) || 0) * Math.PI / 180;
                const zRotation = (parseFloat(document.getElementById('label-z-rotation').value) || 0) * Math.PI / 180;

                const vector = new THREE.Vector3(
                    dist[keys[0]] + xOffset,
                    dist[keys[1]] + yOffset,
                    dist[keys[2]] + zOffset
                ).project(camera);
                const x = (vector.x * 0.5 + 0.5) * (window.innerWidth - 300);
                const y = -(vector.y * 0.5 - 0.5) * window.innerHeight;
                labelDiv.style.transform = `translate(-50%, -50%) rotateX(${xRotation}rad) rotateY(${yRotation}rad) rotateZ(${zRotation}rad)`;
                labelDiv.style.left = `${x}px`;
                labelDiv.style.top = `${y}px`;
            }

            updateLabelPosition();
            window.addEventListener('resize', updateLabelPosition);
            labelUpdateFunctions.push(updateLabelPosition);

            // Add event listeners for offset and rotation changes
            ['label-x-offset', 'label-y-offset', 'label-z-offset',
             'label-x-rotation', 'label-y-rotation', 'label-z-rotation'].forEach(id => {
                document.getElementById(id).addEventListener('input', updateLabelPosition);
            });
        }
    });

    console.log('Created', points.length, 'points');
}

function populateQuestionSelect() {
    console.log('Starting to populate question select');
    const select = document.getElementById('question-select');
    console.log('Found select element:', select);
    console.log('Data length:', data.length);
    
    // Clear existing options
    select.innerHTML = '';
    
    data.forEach((item, index) => {
        console.log('Adding option for question:', item.num, item.question);
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `Question ${item.num}: ${item.question}`;
        select.appendChild(option);
    });

    select.addEventListener('change', (e) => {
        console.log('Question selection changed to index:', e.target.value);
        updateQuestion(parseInt(e.target.value));
    });
}

function updateQuestion(index) {
    console.log('updateQuestion called with index:', index);
    currentQuestion = data[index];
    console.log('Current question data:', currentQuestion);
    
    if (!currentQuestion) {
        console.error('No question data found for index:', index);
        return;
    }
    
    if (!currentQuestion.all_distributions) {
        console.error('No all_distributions found in question:', currentQuestion);
        return;
    }

    const distributions = currentQuestion.all_distributions.each_cad_dis;
    console.log('Distributions data:', distributions);
    
    if (!distributions) {
        console.error('No distributions object found');
        return;
    }
    
    if (typeof distributions !== 'object') {
        console.error('Distributions is not an object:', typeof distributions);
        return;
    }

    // Get the keys from the first distribution
    const firstKey = Object.keys(distributions)[0];
    if (firstKey && distributions[firstKey]) {
        const keys = Object.keys(distributions[firstKey]);
        if (keys.length === 3) {
            // Update the labels
            const labels = [
                { text: keys[0], position: new THREE.Vector3(1.12, 0, 0) },
                { text: keys[1], position: new THREE.Vector3(0, 1.12, 0) },
                { text: keys[2], position: new THREE.Vector3(0, 0, 1.12) }
            ];

            // Remove old labels
            document.querySelectorAll('.axis-label').forEach(el => el.remove());

            // Add new labels
            labels.forEach(label => {
                const labelElement = document.createElement('div');
                labelElement.className = 'axis-label';
                labelElement.textContent = label.text;
                labelElement.style.position = 'absolute';
                labelElement.style.color = 'black';
                labelElement.style.fontSize = '32px';
                document.body.appendChild(labelElement);

                function updateLabelPosition() {
                    const vector = label.position.clone().project(camera);
                    const x = (vector.x * 0.5 + 0.5) * (window.innerWidth - 300);
                    const y = -(vector.y * 0.5 - 0.5) * window.innerHeight;
                    labelElement.style.transform = `translate(-50%, -50%)`;
                    labelElement.style.left = `${x}px`;
                    labelElement.style.top = `${y}px`;
                }

                updateLabelPosition();
                window.addEventListener('resize', updateLabelPosition);
            });
        }
    }

    console.log('Updating question text');
    document.getElementById('question-text').textContent = currentQuestion.question;
    console.log('Creating points');
    createPoints(distributions);
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

// Initialize and start animation
console.log('Starting initialization...');
init();
animate(); 