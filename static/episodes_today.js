
function episodesReleasedToday() {

    var today = new Date()
    var dd = today.getDate()
    var mm = today.getMonth()+1

    current_date = dd + '.' + mm + '.'

    console.log("Current date: " + current_date)

    let elements = document.getElementsByTagName("td")
    // let elements = document.querySelectorAll("td")

    //console.log(elements)
    //console.log(document.getElementsByTagName('td').values)

    let element
    let elementRegex = /(\d){0,2}\.(\d){0,2}\./g;

    //console.log(elements)

    // for some reason we have to reverse the loop, otherwise every 2nd "td" element will be skipped.. wtf?
    for (var i = elements.length - 1 ; i >= 0; i--) {
        element = elements[i].innerHTML
        var match = elementRegex.exec(element)

        if (match != null ) {
            episode_date = match[0]

            //console.log(current_date)
            //console.log(element)
            //console.log(episode_date)

            if (episode_date == current_date) {
                //console.log("Today is: " + episode_date)

                // Html code of episode which was released today
                //console.log(elements[i].parentNode)
                var test = elements[i].parentNode
                //var parsed_html_code = test.cloneNode(true)
                //console.log(parsed_html_code)
                
                //console.log(test)
                
                // This one does not work properly, it doesnt include parent tags "tr" and "td" correctly
                //var parsed_html_code = elements[i].parentElement.outerHTML;
                //console.log(parsed_html_code)
                //document.getElementById('tvshows_today episodes-bg').innerHTML = elements[i].parentElement.outerHTML
                document.getElementById('snippet--episodes tvshows_today').appendChild(test)
            }

        }
    }

}

episodesReleasedToday()








