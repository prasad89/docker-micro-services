const apiURL = "http://localhost:8080/users";

function getUserData() {
  fetch(apiURL)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch user data.");
      }
      return response.json();
    })
    .then((data) => {
      const userTable = document.getElementById("userData");
      userTable.innerHTML = "";
      data.forEach((user) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${user.name}</td>
          <td>${user.email}</td>
          <td>${user.phone}</td>
        `;
        userTable.appendChild(tr);
      });
      const table = document.querySelector(".table");
      table.style.display = "table";
    })
    .catch((error) => {
      console.error("Error fetching user data:", error);
    });
}

const showUserButton = document.getElementById("showUserButton");
showUserButton.addEventListener("click", getUserData);
