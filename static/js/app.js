$(function(){
	var make_pull_quotes = function() {
		/*
		 * Finds all elements called .l_quote and turns them into "call out" quotes
		 */
		var pull_quote = $('span.pull_quote').each(function(){
			var $this = $(this);

			var align = $this.hasClass('left') ? 'left' : 'right'; 

			var blockquote = $('<blockquote></blockquote>', {
				class: 'pull_quote ' + align,
				text: $this.text()
			});

			// Prepend to the blockquote to the closest paragraph tag
			blockquote.prependTo($this.closest('p'));
		});
	};

	/* Main */
	make_pull_quotes();
});
