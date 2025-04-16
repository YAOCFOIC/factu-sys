window.addEventListener("load", () => {
  // Función para animar el texto como humo
  const texto = document.getElementById("titulo");
  const parrafo = document.getElementById("parrafo");
  const logo = document.getElementById("logo");

  // Función para aplicar el efecto de "humo" en el texto
  const aplicarEfectoHumo = (elemento) => {
    const letras = elemento.innerText.split('');
    elemento.innerHTML = '';
    letras.forEach((letra, index) => {
      const span = document.createElement('span');
      span.textContent = letra;
      span.style.opacity = '0';
      span.style.animation = `humo 7s ${index * 0.1}s forwards`;
      elemento.appendChild(span);
    });
  };

  // Efecto de rotación 360 grados en 3D para la imagen
  const rotarImagen3D = () => {
    logo.style.animation = 'rotar3D 7s ease-in-out infinite';
  };

  // Animar texto y logo al aparecer en la vista
  const opciones = {
    root: null,
    rootMargin: '0px',
    threshold: 0.5
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        aplicarEfectoHumo(texto);
        aplicarEfectoHumo(parrafo);
        rotarImagen3D();
        observer.unobserve(entry.target); // Deja de observar una vez se active
      }
    });
  }, opciones);

  observer.observe(texto); // Inicia la observación del texto
});