document.addEventListener('DOMContentLoaded', function() {

	// Add 'onsubmit' property to like buttons
	document.querySelectorAll('.like-form').forEach(function(likeForm) {
		likeForm.onsubmit = function() {
			add_like(likeForm.dataset.postid);
			return false;
		};
	});
});


function add_like(post) {
	fetch('like', {
		method: 'POST',
		body: JSON.stringify({
			post: post,
			other: "foo",
			bar: "baz"
		})
	})
	.then(response => {
		return response.json()
	})
	.then(data => {
		console.log(data.message);
	});
}