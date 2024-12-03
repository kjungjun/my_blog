document.addEventListener("DOMContentLoaded", function () {
    const postsContainer = document.getElementById("posts");

    // 포스트 삭제 버튼 클릭 이벤트 리스너
    postsContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-button")) {
            const postElement = event.target.closest(".post");
            const postId = postElement.dataset.id;

            fetch(`/delete/${postId}`, {
                method: "DELETE"
            })
            .then(response => {
                if (response.ok) {
                    postElement.remove();
                } else {
                    alert("Failed to delete post.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred while deleting the post.");
            });
        }
    });
});
