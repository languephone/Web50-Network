document.addEventListener('DOMContentLoaded', function() {

	// display_posts();
	editPosts();

	// Add 'onsubmit' property to like buttons
	
	// setTimeout(function() {
	// 	document.querySelectorAll('.like-form').forEach(function(likeForm) {
	// 		likeForm.onsubmit = function() {
	// 			add_like(likeForm.dataset.postid);
	// 			return false;
	// 		};
	// 	});
	// }, 1000);
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


function get_posts() {
	fetch('posts')
	.then(response => {
		return response.json()
	})
	.then(data => {
		console.log(data);
	});
}


function display_posts() {
	fetch('posts')
	.then(response => {
		return response.json()
	})
	.then(posts => {
		posts.forEach(function(post) {
		
		// Create variable for section to hold post info
		const posts_div = document.querySelector('.posts');

		// Create HTML elements to hold each post
		const post_div = document.createElement('div');

		const post_username = document.createElement('span');
		const post_content = document.createElement('span');
		const post_date = document.createElement('span');
		const post_like_form = document.createElement('form');
		const post_submit = document.createElement('input');
		const post_like_count = document.createElement('span');

		// Add to inner HTML of each element
		post_username.innerHTML = post.user;
		post_content.innerHTML = post.content;
		post_date.innerHTML = post.date;
		post_submit.value = post.likes;

		// Add classes and attributes to elements
		post_div.classList.add('post');
		post_username.classList.add('post-username');
		post_content.classList.add('post-content');
		post_date.classList.add('post-date');
		post_like_form.classList.add('like-form');
		
		post_like_form.setAttribute('data-postid', post.id);
		post_submit.type = "submit";
		post_submit.name = "like";
		
		const submit_classes = ['post-likes', 'btn', 'btn-primary', 'btn-sm'];
		submit_classes.forEach(function(addClass) {
			post_submit.classList.add(addClass);
		});

		// Append input to form
		post_like_form.append(post_submit);

		// Append each element to the parent div
		post_div.append(post_username);
		post_div.append(post_content);
		post_div.append(post_date);
		post_div.append(post_like_form);
		

		// Add post div to the page
		posts_div.append(post_div);

		// Add event listener to call ajax function and prevent HTML submission
		post_like_form.onsubmit = function() {
				add_like(this.dataset.postid);
				return false;
			};

		});
	});
}

function editPosts() {
	document.querySelectorAll('.edit-likes').forEach(function(editButton) {
		editButton.addEventListener('click', function() {
			fetch('posts', {
				method: 'PUT',
				body: JSON.stringify({
					content: editButton.dataset.content,
					id: editButton.dataset.id
				})
			})
			.then(response => response.json())
			.then(data => {
				console.log(data);
			});
		});
	});
}