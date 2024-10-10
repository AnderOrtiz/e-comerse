document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('userForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

        // Recoger datos del formulario
        const name = document.getElementById('name').value;
        const last_name = document.getElementById('last_name').value;
        const email = document.getElementById('email').value;
        const gender = document.getElementById('gender').value;
        const age = parseInt(document.getElementById('age').value); // Convertir a número

        // Obtener el valor del campo car y manejar el caso vacío
        const carInput = document.getElementById('car');
        const carValue = carInput ? carInput.value.trim() : null; // Verificar si carInput existe

        // Usa null si el valor del campo car está vacío
        const car = carValue && carValue.length > 0 ? carValue.split(',').map(item => item.trim()) : null; 

        const password = document.getElementById('password').value;

        // Crear un objeto para enviar
        const data = { name, last_name, email, gender, age, car, password };

        // Realizar una solicitud POST a tu API de FastAPI
        try {
            const response = await fetch('http://localhost:8000/user/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                document.getElementById('response').innerText = `Usuario ${result.name} creado exitosamente`;
                alert(`Usuario ${result.name} creado exitosamente`)
            } else {
                document.getElementById('response').innerText = `Error: ${result.detail}`;
            }
        } catch (error) {
            document.getElementById('response').innerText = 'An error occurred';
            console.error('Error:', error);
        }
    });
});
