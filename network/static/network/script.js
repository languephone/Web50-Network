document.addEventListener('DOMContentLoaded', function() {

	display_posts();
	
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
		// const post_like_form = document.createElement('form');
		// const post_id = document.createElement('input');
		// const post_like_count = document.createElement('span');

		post_username.innerHTML = post.user;
		post_content.innerHTML = post.content;
		post_date.innerHTML = post.date;

		post_username.classList.add('post-username');
		post_content.classList.add('post-content');
		post_date.classList.add('post-date');

		// Append each element to the parent div
		post_div.append(post_username);
		post_div.append(post_content);
		post_div.append(post_date);
		post_div.classList.add('post');

		// Add post div to the page
		posts_div.append(post_div);

  //           <form class="like-form" data-postid ="{{ post.id }}">
  //               {% csrf_token %}
  //               <input type="hidden" name="post" value="{{ post.id }}">
  //               <input type="submit" name="like" value="Like" class="post-likes btn btn-primary btn-sm">
  //           </form>
  //           <span>{{ post.count_likes }}</span>
		});
	});
}