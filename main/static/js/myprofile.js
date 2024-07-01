document.getElementById('profile-img-upload').addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profile-img').src = e.target.result;
            document.getElementById('home-profile-img').src = e.target.result; // Update home profile image
        }
        reader.readAsDataURL(file);
    }
});

function toggleEditable(fieldId) {
    const field = document.getElementById(fieldId);
    if (field.hasAttribute('readonly')) {
        field.removeAttribute('readonly');
        field.focus();
    } else {
        field.setAttribute('readonly', true);
    }
}

document.getElementById('profile-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    fetch("{% url 'update_profile' %}", {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('사진이 성공적으로 바뀌었다람쥐');
            // Update the profile picture on the home page if necessary
            document.getElementById('home-profile-img').src = document.getElementById('profile-img').src;
        } else {
            alert('사진 업로드에 실패하였습니다. 다시 시도하여주세요.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('에러에러에러에러에러에러.');
    });
});
