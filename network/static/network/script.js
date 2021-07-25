document.addEventListener('DOMContentLoaded', function() {

	// Add event listeners for editing & liking posts
	editPostsFunctionality();
	likePostsFunctionality();

});


function updateLike(post) {
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

function editPostsFunctionality() {
	document.querySelectorAll('.post-edit').forEach(link => {
		link.onclick = function() {
			editPost(link.dataset.id);
			return false;
		}
	});
};


function likePostsFunctionality() {
	document.querySelectorAll('.like-update').forEach(form => {
		form.onsubmit = function() {
			likePost(form.dataset.id);
			return false;
		}
	});
}


function likePost(id) {
	fetch('like', {
		method: 'POST',
		body: JSON.stringify({
			id: id
		})
	})
	.then(response => response.json())
	.then(data => {
		console.log(`Liked post ${id}.`);
		
		// Update like count and text of like button
		const postLikes = document.querySelector(`#post${id} h6`);
		postLikes.innerHTML = `Likes: ${data.current_likes}`;
		const likeButton = document.querySelector(`#post${id} .post-likes`);
		if (data.is_liked === true) {
			likeButton.value = 'Unlike';
			likeButton.classList.remove('btn-primary')
			likeButton.classList.add('btn-outline-primary')
		} else {
			likeButton.value = 'Like';

		}
	});
}


function updatePost(content, id) {
	fetch('posts', {
		method: 'PUT',
		body: JSON.stringify({
			content: content,
			id: id
		})
	})
	.then(response => response.json())
	.then(data => {
		console.log(`Successfully updated post to '${data}'`);
		const postContent = document.querySelector(`#post${id} .post-content`);
		postContent.innerHTML = data;
	});
}


function editPost(postId) {
	
	const postSpan = document.querySelector(`#post${postId} .post-content`);
	const postLink = document.querySelector(`#post${postId} .post-edit`)
	const postContent = postSpan.innerHTML;

    // Hide edit link to prevent double-editing
    postLink.style.display = 'none';

	// Create form to allow editing post
	newInput = document.createElement('textarea');
	newSubmit = document.createElement('button');

	// Style new elements
	newInput.value = postContent;
	newInput.cols = '40';
	newInput.rows = '3';

	newSubmit.type = 'button';
	newSubmit.innerHTML = 'Submit';
	newSubmit.classList.add('btn');
	newSubmit.classList.add('btn-secondary');
	newSubmit.classList.add('btn-sm');

	// Append form to existing div
	postSpan.innerHTML = '';
	postSpan.append(newInput)
	postSpan.append(newSubmit);

	// Add function to call when submitting form
	newSubmit.onclick = function() {

		const content = newInput.value;

		// Re-show edit link
		postLink.style.display = 'inline';

		// Call function to update sql
		updatePost(content, postId);

		// Prevent link from being followed
		return false;
	}
};