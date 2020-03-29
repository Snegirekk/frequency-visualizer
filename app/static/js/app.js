$(document).ready(function () {
  bsCustomFileInput.init()

  $('form').submit(() => {
    let html = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;wait...'

    $(this).find('button')
        .attr('disabled', true)
        .html(html)
  })
})