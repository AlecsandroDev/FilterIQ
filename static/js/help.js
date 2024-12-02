document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("btn_talk").addEventListener("click", function () {
    axios
      .get("http://localhost:5000/talk")
      .then(function (response) {
        window.location.href = 'http://localhost:5000/talk';
      })
      .catch(function (error) {
        console.log("Erro na requisição:", error)
      })
  })
});
