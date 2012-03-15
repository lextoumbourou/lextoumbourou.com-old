$(function() {
	var makePullQuotes = function() {
		/*
		 * Finds all elements called .pull_quote and turns them into "call out" quotes
		 * used for making quotes pop in articles
		 */
		var pullQuote = $('span.pull_quote').each(function(){
			var $this = $(this);

			// checks if an additional alignment class has been specified
			var align = $this.hasClass('left') ? 'left' : 'right'; 

			var blockquote = $('<blockquote></blockquote>', {
				class: 'pull_quote ' + align,
				text: $this.text()
			});

			// Prepend to the blockquote to the closest paragraph tag
			blockquote.prependTo($this.closest('p'));
		});
	};

	var pageTransition = function() {
		/*
		 * Accepts a container div and an element found the container
		 * that when clicked on, will fade all the other elements
		 * and slide to the top of the screen
		 */

		var titles = $('.title');
		titles.on('click', 'a', function(e) {
			e.preventDefault();
			// Get all <li>s except the one that holds the current element
			// and fade them out
			$(this)
				.parents('li')
					.siblings()
					.fadeOut(1000);
		});

	};
	pageTransition()
	makePullQuotes();
});
