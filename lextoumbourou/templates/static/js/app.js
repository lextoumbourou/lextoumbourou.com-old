/*
 * I, Lex Toumbourou, hereby solemnly swear to refactor this code...
 */
$(function() {
    $(document).ready(function() {
            var articles = $('ul.articles');
            var lastHr = $('hr').last();

            articles.css('opacity', 0);
            lastHr.css('display', 'none')

            articles.animate({'opacity':1},(1500))
            lastHr.fadeIn(2500);

            $('div.article_body').css('display', 'none').fadeIn(1500).slideDown(1500);
    });

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

    var pageTransition = function(list) {
            /*
             * Various transistion effects
             */
            var ul = $(list);
            var lis = ul.children();
            var titles = lis.children('.title');

            // Set each list item to absolute positions
            lis.each(function() {
                    var h = $(this).position().top;
                    $(this).css('top', h+'px');
            });
            
            var topPos = lis.eq(0).position();

            titles.on('click', 'a', function(e) {
                    e.preventDefault();
                    var url = $(this).attr('href');
                    $self = $(this);
                    $('hr').last().fadeOut('fast', function(){
                            lis.css('position', 'absolute');
                            $self
                                    .parents('li')
                                    .siblings()
                                            .fadeOut('slow')
                                            .end()
                                            .animate(
                                                    {top:topPos.top},
                                                    1000,
                                                    function() {
                                                            window.location.replace(url);
                                                    }
                                            );
                    });
                    
            });

            $('h1').on('click', 'a', function(e) {
                    e.preventDefault();
                    var url = $(this).attr('href');
                    $('div#content').animate({'opacity':0}, 1000, function() {
                            window.location.replace(url);
                    });

            });

    };

    pageTransition('ul.articles');
    makePullQuotes();
});
