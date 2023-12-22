/* jshint esversion: 8 */
$(document).ready(function () {
  $(document).on("keyup change", "#projectsearch", function (e) {
    const search = $(this).val();
    if (!search || search === "") {
      $(".project-container").removeClass("d-none");
    } else {
      $(".project-container").each(function () {
        if ($(this).data("name").toLowerCase().includes(search.toLowerCase())) {
          $(this).removeClass("d-none");
        } else {
          $(this).addClass("d-none");
        }
      });
    }
  });
});
