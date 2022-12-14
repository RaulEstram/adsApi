/*

  VARIABLES QUE SE ESTARAN USANDO GLOBALMENTE

*/
console.log("hola3");
const endpoint = "";
const $alert = document.getElementById("alert"),
  $main = document.getElementById("main"),
  $loadtable = document.getElementById("loadtable"),
  $btnBuscar = document.getElementById("btnBuscar"),
  $tableBody = document.getElementById("main-table-body"),
  $entry = document.getElementById("entry"),
  $message = document.getElementById("message"),
  $saveButton = document.getElementById("ok-modal");
let dataArticles = {};

/*

FUNCIONES PARA MOSTRAR MENSAJES Y ERRORES

*/

function showMessage(text) {
  $alert.innerHTML =
    `<div class="alert alert-success alert-dismissible fade show align-items-center fixed fix-message centrar-alert" role="alert">
    <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
      <use xlink:href="#check-circle-fill" />
    </svg>
    <strong>Exito: </strong> ` +
    text +
    `
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  </div>`;
  setTimeout(() => {
    $alert.innerHTML = "";
  }, 5000);
}

function showError(error) {
  $alert.innerHTML =
    `<div class="alert alert-danger alert-dismissible fade show align-items-center fixed fix-message centrar-alert" role="alert">
    <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
    <use xlink:href="#exclamation-triangle-fill"/>
    </svg>
    <strong>Error: </strong> ` +
    error +
    `
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  </div>`;
  setTimeout(() => {
    $alert.innerHTML = "";
  }, 5000);
}

/*

COMPROBAR SI EL USUARIO SI ES VALIDO

*/

// Ejecucion de funcion anonima autoejecutable para saber si el usuario es valido
window.addEventListener("load", (e) => {
  async function getAuthorization() {
    try {
	let end = endpoint + "/user/" + id;
      let response = await fetch("/user/" + id),
        data = await response.json();
      if (data.status) {
        $main.classList.remove("hidden-content");
      } else {
        $main.innerHTML = ``;
        $alert.innerHTML = ` <div class="alert alert-danger" role="alert"> <h4 class="alert-heading"> <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"> <use xlink:href="#exclamation-triangle-fill" /> </svg> Hay un error :( </h4> <p> Para que el contenido de esta p??gina sea visible deber??as de acceder desde un usuario v??lido o desde la p??gina oficial. </p> <hr /> <p class="mb-0"> Prueba a ingresar a la p??gina desde <a href="https://www.google.com/">aqu??</a> </p> </div>`;
      }
    } catch (error) {
      $main.innerHTML = ``;
      $alert.innerHTML = ` <div class="alert alert-danger" role="alert"> <h4 class="alert-heading"> <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"> <use xlink:href="#exclamation-triangle-fill" /> </svg> Hay un error :( </h4> <p> Es posible que los servicios ADS no se encuentren disponibles en estos momentos. </p> <hr /> <p class="mb-0"> Prueba a ingresar a la p??gina desde <a href="https://www.google.com/">aqu??</a> </p> </div>`;
    }
  }

  getAuthorization();
});

/* 

FUNCIONAMIENTO DE BUSQUEDA DE ARTICULOS MEDIANTE EL USO DE LA API

*/

// elementos necesarios

$btnBuscar.addEventListener("click", async (e) => {
  // evitamos el funcionamiento por defecto del evento
  e.preventDefault();

  if ($entry.value === "") {
    showError("Ingrese una llave a buscar.");
    return;
  }

  if ($entry.value.length < 4) {
    showError("La llave a buscar tiene que ser de m??nimo 4 caracteres.");
    return;
  }

  // funcion async que realizara la peticion HTTPs
  async function getData() {
    try {
      $tableBody.innerHTML = "";
      $loadtable.innerHTML = `<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>`;
      // realizamos la peticion con fetch
      let response = await fetch(endpoint + "/search/" + $entry.value),
        data = await response.json();
      // comprobamos que la peticion se realizo correctamente
      if (!data["status"]) {
        throw { message: "Error al realizar la b??squeda" };
      }

      $fragment = document.createDocumentFragment();

      for (const element in data.data) {
        const article = data.data[element];
        $tr = document.createElement("tr");
        $tr.innerHTML =
          `
          <th>` +
          element +
          `</th>
          <th>` +
          article.authors +
          `</th>
          <th>` +
          article.title +
          `</th>
          <th>` +
          article.pub +
          `</th>
          <th>` +
          article.url +
          `</th>
          <th>` +
          article.bibcode +
          `</th>
          <th>` +
          article.doi +
          `</th>
          <th>` +
          article.page_range +
          `</th>
          <th>` +
          article.volume +
          `</th>
          <th>` +
          article.year +
          `</th>
          <th><button type="button" data-bs-toggle="modal" data-bs-target="#staticBackdrop" class="btn btn-primary save-button-table" data-id=` +
          element +
          `>Guardar</button></th>`;
        $fragment.appendChild($tr);
      }
      $loadtable.innerHTML = ``;
      $tableBody.appendChild($fragment);
      dataArticles = data.data;
    } catch (error) {
      showError("Se produjo un error inesperado: " + error.message);
    }
  }
  getData();
});

/* 

Realizar peticion para guardar Datos

*/

document.body.addEventListener("click", async (e) => {
  // accion si se da click en boton de guardar un articulo
  if (e.target.matches(".save-button-table")) {
    let id_art = e.target.dataset.id;
    $saveButton.dataset.id = id_art;
    document.getElementById("text-modal").innerHTML =
      `Est?? seguro que quiere Guardar el art??culo: <br><br>` +
      dataArticles[id_art].title +
      `<br><br>Si ya lo tiene registrado se actualizar?? con la informaci??n que est?? en esta p??gina, de lo contrario se guardara.`;
    $saveButton.classList.add("save-article");
  }

  // accion si se da click en boton de guardar todos los articulo
  if (e.target.matches("#save-all")) {
    $saveButton.dataset.id = id;
    $saveButton.dataset.all = true;
    document.getElementById("text-modal").innerHTML =
      "??Est?? Seguro que quiere guardar todos los art??culos que aparecen?<br><br>Los art??culos que ya tenga registrados se actualizaran con la informaci??n que aparece en esta p??gina, de lo contrario se guardara, por lo que se recomienda guardarlos uno por uno.";
    $saveButton.classList.add("save-all-articles");
  }

  // guardar archivo
  if (e.target.matches("#save-sql")) {
    $saveButton.dataset.id = id;
    $saveButton.dataset.all = true;
    document.getElementById("text-modal").innerHTML =
      "??Est?? Seguro que quiere guardar un archivo sql?<br><br>Estos archivos NO son perfectos, por lo que podrian llegan a tener algun error en la sintaxis debido a los valores del articulo, es recomendable que se revisen";
    $saveButton.classList.add("save-sql-file");
  }

  
  // acction por si se salen del modal
  if (e.target.matches(".cancel-button")) {
    removeData();
  }

  // accion para guardar un solo articulo
  if (e.target.matches(".save-article")) {
    saveArticle(e.target.dataset.id);
    removeData();
  }
  // accion para guardar todos los articulos
  if (e.target.matches(".save-all-articles")) {
    saveAllArticles();
    removeData();
  }

  if (e.target.matches(".save-sql-file")) {
    saveSqlFile();
    removeData();
  }
});

async function request(url, body, update = false) {
  try {
    let method = "POST";
    if (update) {
      method = "PUT";
    }

    let response = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }),
      data = await response.json();
    return data;
  } catch (error) {
    throw { message: "Error al realizar la petici??n." };
  }
}

function removeData() {
  $saveButton.classList.remove("save-article");
  $saveButton.classList.remove("save-all-articles");
  $saveButton.classList.remove("save-sql-file");
  $saveButton.removeAttribute("data-all");
  $saveButton.removeAttribute("data-id");
}

async function saveArticle(id_art) {
  try {
    let data = await request(endpoint + "/userarticle", {
      user_id: id,
      bibcode: dataArticles[id_art].bibcode,
    });

    const url = endpoint + "/article";
    const body = structuredClone(dataArticles[id_art]);
    body.user_id = id;
    let response;

    if (!data.status) {
      response = await request(url, body);
    } else {
      body.update = true;
      response = await request(url, body, (update = true));
    }
    if (response.status) {
      showMessage(response.message);
    } else {
      showError(response.error);
    }
  } catch (error) {
    showError("Error al Guardar el art??culo.");
  }
}

async function saveAllArticles() {
  try {
    const url = endpoint + "/articles";
    const body = {
      data: structuredClone(dataArticles),
      user_id: id,
    };
    const data = await request(url, body);

    if (data.status) {
      showMessage(
        "Se Insertaron " +
          data.inserts +
          " Art??culos, Se actualizaron " +
          data.updates +
          " Art??culos y se produjeron " +
          data.errors +
          " Errores."
      );
    } else {
      showError(data.error);
    }
  } catch (error) {
    showError("Error al guardar todos los Art??culos.");
  }
}

async function saveSqlFile() {
  try {
    const url = endpoint + "/queries";
    const body = {
      data: structuredClone(dataArticles),
      user_id: id,
    };
    
    const data = await request(url, body);

    let response = await fetch(endpoint + "/downloads/" + data.filename);

    if(response.statusText !== "OK") throw "error archivo"

    if (!response.redirected) {
      window.location.href = response.url;
    }

  } catch (error) {
    console.log(error);
    showError("No hay ningun Articulo con el cual podamos crear un archivo sql, prueba realizando una busqueda.");
  }
}


