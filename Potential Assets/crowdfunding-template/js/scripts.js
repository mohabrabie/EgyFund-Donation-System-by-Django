$(function(){

    // Configure tabs
    $('.tabs__tab a').on('click', function (e) {
        e.preventDefault();
        $('.tabs__content').removeClass('tabs__content--active');
        $($(this).attr('href')).addClass('tabs__content--active');
        $('.tabs__tab').removeClass('tabs__tab--active');
        $(this).closest('.tabs__tab').addClass('tabs__tab--active');
    })

    // Show pledge dialog
    $('.btn--pledge, .reward').on('click', function (e) {
        e.preventDefault();
        if ($(this).is(':not([disabled])')) {
            var reward = $(this).data('reward');
            $('.pledge__form select[name=reward]').val(reward).change();
            $('html').addClass('modal-open');
        }
    })

    // Hide pledge dialog
    $('.modal__cancel').on('click', function (e) {
        e.preventDefault();
        // Hide the modal
        $('html').removeClass('modal-open');
        // Reset the form
        $('.pledge__form')[0].reset()
        // Show/hide form and thank you message
        $('.pledge__form').show();
        $('.pledge__thank-you').hide();
    })

    // Handle pledge button click
    $('.pledge__submit').on('click', function (e) {
        e.preventDefault();
        var formEl = $('.pledge__form')[0];
        if (formEl.checkValidity()) {
            // TODO: Peform the pledge action
            $('.pledge__form').hide();
            $('.pledge__thank-you').show();
        }
    })

    // Listen for changes to reward dropdown and auto update amount field
    $('.pledge__form select[name=reward]').on('change', function () {
        var opt = $(this).find('option[value="'+ $(this).val() + '"]');
        var amt = Number('0' + opt.data('amount'));
        $('.pledge__form input[name=amount]').attr('min', amt).val(amt);
    });

    // Set default values on form reset
    $('.pledge__form').on('reset', function () {
        var form = this;
        setTimeout(function () {
            $(form).find('input.default-checked').prop('checked', true);
        }, 1);
    })

    // Little helper to track dirty inputs
    $('form input, form select, form textarea').on('blur valid invalid', function() {
        $(this).addClass('dirty');
    });
    $('form').on('reset', function () {
        var form = this;
        setTimeout(function (){ 
            $(form).find('.dirty').removeClass('dirty');
        }, 1)
    })

    // Track checkboxes that default to checked
    $('input[checked]').each(function (idx, itm) {
        $(itm).addClass('default-checked');
    })

});