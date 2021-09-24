var requesting = false;
var bar =
  '<li><div data-percentage="_PER_" class="bar"></div><span>_NAM_</span></li>';
var bar_prob = "_PER_";
var bar_name = "_NAM_";
var colors = [
  "009DE0",
  "46962b",
  "000000",
  "DF0404",
  "FFED00",
  "FF8800",
  "E3000F",
];
$("#requester").submit(function (event) {
  event.preventDefault();
  account = $("#requester-name").val().replace(/\s/g, "").replace("@", ""); //Remove all whitespaces
  console.log("submitted " + account);
  if (account == "") {
    console.log("Error: Empty namefield");
    return;
  }
  if (requesting) return;
  requesting = true;
  /*if (!twitterNameExists(account)) {
				// meldung, dass name nicht existiert
				requesting = false;
				return;
			}*/

  $("#internal-error:not(.gone)").addClass("gone");
  $("#loadingresults.gone").removeClass("gone");
  var calling =
    "https://api.chirpanalytica.com/de/predictuser?handle=" + account;
  console.log(calling);

  _paq.push(["trackEvent", "Predict", "Account", account]); //Matomo Tracking
  $.ajax({
    url: calling,
    context: document.body,
  })
    .done(function (values) {
      $("#loadingresults:not(.gone)").addClass("gone");
      if (values["success"] == false) {
        $("#requester-name").effect("highlight", { color: "#f99" }, 1500);
        requesting = false;
      } else {
        $("#chart.gone").removeClass("gone");
        values = values["data"];
        console.log(values);
        $("#bars").html("");
        for (key in values) {
          newBar = bar.replace(
            bar_name,
            key.replace(new RegExp("B.*90.*", "gm"), "Die Grünen")
          );
          newBar = newBar.replace("Alternative für Deutschland", "AfD");
          newBar = newBar.replace(
            "Christlich Demokratische Union Deutschlands",
            "CDU"
          );
          newBar = newBar.replace("Freie Demokratische Partei", "FDP");
          newBar = newBar.replace(
            "Piratenpartei Deutschland",
            "Piraten-<br>partei"
          );
          newBar = newBar.replace(
            "Sozialdemokratische Partei Deutschlands",
            "SPD"
          );
          newBar = newBar.replace(bar_prob, Math.round(values[key] * 100));
          $("#bars").html($("#bars").html() + newBar);
        }
        $(function () {
          $("#bars li .bar").each(function (key, bar) {
            bar.style.background = "#" + colors[key];
            var percentage = $(this).data("percentage");
            $(this).css("height", "0px");
            $(this).animate(
              {
                height: percentage + "%",
              },
              1000
            );
          });

          requesting = false;
        });
      }
    })
    .fail(function (values) {
      $("#internal-error.gone").removeClass("gone");
      $("#loadingresults:not(.gone)").addClass("gone");
      requesting = false;
    });
});
