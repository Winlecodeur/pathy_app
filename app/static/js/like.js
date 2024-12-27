
document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll(".like-btn");

    likeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const postId = this.dataset.postId;
            const likeIcon = document.getElementById(`like-icon-${postId}`);
            const likeCount = document.getElementById(`like-count-${postId}`);

            fetch(`like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                }
            })
            .then(response => response.json())
            .then(data => {
                // Change l'image
                likeIcon.src = data.liked 
                    ? "{% static 'like_full.png' %}" 
                    : "{% static 'like_empty.png' %}";
                // Met à jour le compteur
                likeCount.textContent = data.total_likes;
            })
            .catch(error => console.error("Erreur:", error));
        });
    });
});