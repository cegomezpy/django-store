$(document).ready(function () {
    var rating = 5;

    $('#product-rating').val(rating)
    $('.star-comment').click(function () {
        var index = $(this).data('index');
        if ($(this).hasClass('fas-star')) {
            $(this).removeClass('fas').addClass('far');
        } else {
            $(this).removeClass('far').addClass('fas');
        }
        $(this).prevAll().removeClass('far').addClass('fas');
        $(this).nextAll().removeClass('fas').addClass('far');
        rating = index
        $('#product-rating').val(rating)
        console.log("rating is", $('#product-rating').val())
    });

    // Click submit button
    $("#review-form").submit(function (event) {
        // Prevent default form submission behavior
        event.preventDefault();

        // Submit form data using Ajax
        $.ajax({
            type: "POST",
            url: "/Store/Details/review/",
            headers: {
                'X-CSRFToken': $(this).attr('data-csrftoken'),
            },
            data: $(this).serialize(),
            success: function (response) {
                // Handle success response
                if (response.message){
                    pop_message(response);
                } else {
                    update_review(response);
                    update_review_length('review-length-review');
                    update_review_length('review-length-details');    
                }
            },
            error: function (xhr, status, error) {
                // Handle error response
            }
        });

        function update_review_length(target_id){
            // Get the text content of the #reviews-length-update element
            var reviewLength = $('#'+target_id).text();

            // Use a regular expression to extract the first number from the text
            var firstNumber = parseInt(reviewLength.match(/\d+/)[0]);

            // Add 1 to the first number
            var newNumber = firstNumber + 1;

            // Concatenate the new value with the other text that appears
            var newContent = reviewLength.replace(reviewLength.match(/\d+/)[0], newNumber);

            // Update the #reviews-length-update element with the new content
            $('#'+target_id).text(newContent);
        }

        function update_review(response){
            // Create a new HTML element using jQuery and set its class and ID attributes
            var newDiv = $('<div>').addClass('media mb-4').attr('id', 'review-row-' + response.review_id);

            // Create the inner HTML content using the review object properties and a loop
            var innerHtml = '<div class="media-body">' +
                '<h6>' + response.author + '<small> - <i>' + response.date_created + '</i></small></h6>' +
                '<div class="rating-stars text-primary mb-2">';
            for (var i = 1; i <= 5; i++) {
                if (i <= response.rating) {
                    console.log("Star added")
                    innerHtml += '<i class="fas fa-star"></i>';
                } else {
                    innerHtml += '<i class="far fa-star"></i>';
                }
            };
            innerHtml += '</div><p>' + response.comment + '</p></div>';

            // Set the inner HTML content of the new HTML element using jQuery
            newDiv.html(innerHtml);
           // Append the new HTML element to the page using jQuery
            $('#reviews-section').prepend(newDiv);
        }

        function pop_message(response){
            $('#response-message').text(response.message);
            $('#popup').fadeIn(500).delay(2000).fadeOut(500);
        }
    });
});