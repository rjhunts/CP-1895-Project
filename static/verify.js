document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById('gameForm');

  form.addEventListener('submit', (e) => {

    if (form.action.endsWith("/add")) {
      const imageInput = document.getElementById('gameImage');
      const imageFile = imageInput.files[0];

      if (!imageFile || !['image/jpeg', 'image/png'].includes(imageFile.type)) {
        alert('Only .jpg and .png files are allowed.');
        imageInput.value = '';
        e.preventDefault();
        return;
      }
    }
  })
})