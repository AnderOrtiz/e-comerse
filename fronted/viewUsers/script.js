document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'http://localhost:8000/user/'; // Reemplaza con la URL real de tu API

    // Función para obtener datos de la API
    function fetchUsers() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.querySelector('#userTable tbody');
                tableBody.innerHTML = ''; // Limpiar el contenido previo

                data.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.name}</td>
                        <td>${user.last_name}</td>
                        <td>${user.email}</td>
                        <td>${user.gender}</td>
                        <td>${user.age}</td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    // Llamar a la función para cargar los usuarios al cargar la página
    fetchUsers();
});
