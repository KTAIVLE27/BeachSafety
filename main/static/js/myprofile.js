// 파일 선택 시 프로필 사진 미리보기 및 저장
function previewImage(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function() {
        var dataURL = reader.result;
        var imgElement = document.getElementById('profile-img');
        imgElement.src = dataURL;
    };

    reader.readAsDataURL(input.files[0]);
}

// 비밀번호 확인 및 프로필 저장 기능
function saveProfile() {
    var pwField = document.getElementById('profile-pw');
    var pwConfirmField = document.getElementById('profile-pw-confirm');
    var pwError = document.getElementById('password-error');

    // Check if passwords match
    if (pwField.value !== pwConfirmField.value) {
        pwError.textContent = "비밀번호가 일치하지 않습니다.";
        alert("비밀번호가 일치하지 않습니다.");
        return; // Do not proceed further
    } else {
        pwError.textContent = ""; // Clear error message if passwords match
    }

    // 여기서 프로필 정보를 서버에 전송하여 저장하는 로직을 구현합니다.
    // 예시로 Alert 대신 팝업으로 저장되었음을 표시합니다.
    alert('프로필 수정이 완료되었습니다.');
}
