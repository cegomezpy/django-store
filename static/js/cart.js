$(document).ready(function () {
  var data = {}
  // declare a constant for the debounce update cart
  const debounceUpdateCart = debounce(updateCart, 200);
  // click add_to_cart button
  $('.add-to-cart').click(function () {
    var productId = $(this).attr('data-product-id');
    var csrfToken = $(this).attr("data-csrf-token");
    var quantity = $('#quantity-inpt').val();
    return addToCart(quantity, productId, csrfToken);
  });

  // click cart delete button
  $('.delete-btn').click(function () {
    console.log("Delete button pressed");
    var productId = $(this).attr('product-id');
    return deleteProduct(productId);
  });

  // details input change
  $('#quantity-inpt, .quantity-btn-detail').on('blur click', function() {
    console.log("Quantity button pressed");
    var product_id = $(this).attr('data-product-id');
    var quantity = $('#quantity-inpt').val();
    validateQuant(quantity, product_id);
  });



// cart input change
$('.quantity-inpt').on('blur', function() {
  console.log("Quantity input blurred");
  var product_id = $(this).attr('product-id');
  var quantity = $(this).val();
  var price = $('#price-label-' + product_id).text().slice(1);
  console.log(price);
  // If input is valid send update query
  if (validateQuant(quantity, product_id, price)) {
    debounceUpdateCart();
  }
});
 // cart input change by quantity buttons
$('.quantity-btn').on('click', function() {
  console.log("Quantity button clicked");
  var product_id = $(this).attr('product-id');
  var quantity = $('.quantity-inpt[product-id="' + product_id + '"]').val();
  var price = $('#price-label-' + product_id).text().slice(1);
  console.log(price);
  // If input is valid send update query
  if (validateQuant(quantity, product_id, price)) {
    debounceUpdateCart();
  }
});


 // click shipping button
 $('.shipping-button').on('click', function() {
  var shippingKey = $(this).attr('key');
  var csrfToken = $(this).attr('data-csrf-token');
  selectShipping(shippingKey, csrfToken);
});


// FUNCTIONS

  // Debounce function
  function debounce(func, delay) {
    let timerId;
  
    return function() {
      const context = this;
      const args = arguments;
      
      clearTimeout(timerId);
      timerId = setTimeout(() => {
        func.apply(context, args);
      }, delay);
    };
  }

  // Define a function to update the total value
  function updateTotal() {
    var total = 0;
    $('.p-subtotal').each(function() {
      var subtotal = parseFloat($(this).text().replace('$', ''));
      total += subtotal;
    });
    $('#total-import').text('$' + total.toFixed(2));
  };

  // Validate the input
  function validateQuant(quantity, product_id, price) {
    console.log(quantity);
    var quantity = quantity
    if (Number.isInteger(parseInt(quantity)) && (parseInt(quantity) < 9999999) && (parseInt(quantity) > 0)) {
      console.log("Is valid");
      if (price !== undefined){
        var subtotal = (parseInt(quantity) * parseFloat(price)).toFixed(2);
        // Set the new subtotal value 
        $("#subtotal-"+product_id).text('$' + subtotal);
      }
      data[product_id] = quantity;
      console.log(data);
      return true;
    } else {
      console.log("Not valid");
      if (price === undefined){
        $('#quantity-inpt').val('1');
      }
      else{
        $('.quantity-inpt[product-id="'+product_id+'"]').val(data[product_id]);
      }
      quantity = 1;
      return false;
    }
  };  

  // Add to cart query
  function addToCart(quantity, productId, csrfToken) {
    if (quantity){
      var quantity = quantity;
    } else {
      var quantity = 1;
    };
    $.ajax({
      url: '/Cart/add_to_cart/',
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      data: {
        'product_id': productId,
        'quantity': quantity,
      },
      success: function (response) {
        $('#response-message').text(response.message);
        $('#popup').fadeIn(500).delay(2000).fadeOut(500);
        console.log(response.message);
        if (response.message !== "The product is already in the cart" && response.message !== "There are only "+response.in_stock.toString()+" products left"){
          var quantity_badge = parseInt($('.cart-quantity-badge').text()) + 1;
          $('.cart-quantity-badge').text(quantity_badge);
        }
      },
      error: function (response) {
        $('#response-message').text("An error has ocurred, please add the product again");
        $('#popup').fadeIn(500).delay(2000).fadeOut(500);
      }
    });
  };

  // Update query
  function updateCart() {
    console.log("update sent");
      $.ajax({
        url: '/Cart/update_cart/',
        method: 'POST',
        headers: {
          'X-CSRFToken': $('.table').attr("data-csrf-token")
        },
        data: data,
        async: false,
        success: function(response) {
          console.log(response.message);
          $("#total-import").text('$' + response.total);
        },
        error: function(xhr, status, error) {
          console.error(xhr.responseText);
        }
      });
    };
  
  // Delete product query
  function deleteProduct(product_id) {
    $.ajax({
      url: '/Cart/delete_product/',
      method: 'POST',
      headers: {
        'X-CSRFToken': $('.table').attr("data-csrf-token")
      },
      data: {
        'product_id': product_id,
      },
      success: function(response) {
        console.log(response.message)
        // Remove the table row for the deleted product
        $('#row-' + product_id).remove();
        // Set the new total value 
        $("#total-import").text(response.total);
        var quantity_badge = parseInt($('.cart-quantity-badge').text()) - 1;
        $('.cart-quantity-badge').text(quantity_badge);
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }
  // Select shipping
  function selectShipping(shippingKey, csrfToken) {
    $.ajax({
      url: '/Cart/set_shipping/',
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      },
      data: {
        'shippingKey': shippingKey,
      },
      success: function(response) {
        $('#shipping-tag').text(response.key);
        $('#shipping-value').text('$' + response.shipping_price);
        $("#total-import").text('$' + response.total);
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }

});