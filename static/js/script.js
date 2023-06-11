const form = document.querySelector('form');
const container = document.querySelector('.container');

form.addEventListener('submit', function(event) {
  // Предотвращаем стандартное поведение отправки формы
  event.preventDefault();

  const formData = new FormData(form);
  const url = formData.get("url")
  const queryString = "/url=" + fixedEncodeURIComponent(url);
  // Отправляем запрос AJAX, используя полученные данные формы.
  // Например, можно отправить запрос на сервер с помощью fetch.
  fetch(queryString, {
    method: "POST",
    body: formData,
  })
  .then(response => {
      if (!response.ok) {
        throw new Error("Ошибка при выполнении запроса");
      }
      return response.json();
    })
  .then(data => {
    const shortUrl = data.shorten_url;

    let resultElement = document.querySelector("#short-url");
    let resultTextElement = document.querySelector("#result");


    if (!resultElement) {
      resultElement = document.createElement("span");
      resultElement.id = "short-url";
      document.body.appendChild(resultElement);
    }

    resultTextElement.textContent = "Short URL: ";
    resultElement.textContent = shortUrl;

    // Копируем в буфер при клике по элементу
    resultElement.addEventListener('click', function() {
        navigator.clipboard.writeText(shortUrl)
          .then(() => {
            console.log("URL скопирован в буфер обмена");
          })
          .catch(error => {
            console.log("Ошибка при копировании URL в буфер обмена:", error);
          });
      });
  })
  .catch(error => {
    console.log("Произошла ошибка при выполнении запроса:", error);
  });
});

// Заменяет все символы, которые не допустимы в URI, на их коды в формате %XY
// где XY - это шестнадцатеричное представление кода символа
function fixedEncodeURIComponent (str) {
  return encodeURIComponent(str).replace(/[!'()*/]/g, function(c) {
    return '%' + c.charCodeAt(0).toString(16);
  });
}
