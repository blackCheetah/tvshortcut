
// Extending string fucntion
// E.g. '{}'.format(string)
String.prototype.format = function () {
    var args = [].slice.call(arguments);
    return this.replace(/(\{\d+\})/g, function (a){
        return args[+(a.substr(1,a.length-2))||0];
    });
};


function episodesReleasedToday() {

    var today = new Date()
    var dd = today.getDate()
    var mm = today.getMonth()+1

    current_date = dd + '.' + mm + '.'

    console.log("Current date: " + current_date)

    let elements = document.getElementsByTagName("td")

    let element
    let elementRegex = /(\d){0,2}\.(\d){0,2}\./g;
    //let elementRegex = /16\.10\./g

    // for some reason we have to reverse the loop, otherwise every 2nd "td" element will be skipped.. wtf?
    for (var i = elements.length - 1 ; i >= 0; i--) {
        element = elements[i].innerHTML

        //console.log(element)

        var match = elementRegex.exec(element)
        
        console.log(match)

        if (match != null ) {

            var episode_date = match[0]

            //console.log(match)

            if (episode_date == current_date) {

                todays_episode_element = elements[i].parentNode.innerHTML
                todays_episode_node = elements[i].parentNode

                //console.log(todays_episode_element)
                //console.log(todays_episode_node)

                var tvshow_name = todays_episode_node.getElementsByTagName('a').title

                //var tvshow_name = "test"

                // Hotfix for duplicate elemenets to be skipped. 
                // kinda hacky way, but hey.. it works :-)
                var td_id = 'snippet--episodes {0}'.format(tvshow_name)

                //console.log("td_id: ", td_id)
                //console.log("parentNode.id: ", todays_episode_node.parentNode.id)

                if (todays_episode_node.parentNode.id == td_id) { // check comment on line 48
                    continue;
                }

                var title = todays_episode_node.parentNode.parentNode.parentElement.getElementsByTagName('h2')[0].textContent //.getElementsByTagName('h2')[0].innerHTML

                var h2_element = document.createElement('h2')
                var h2_title_node = document.createTextNode(title)
                h2_element.appendChild(h2_title_node)
                var div_tvshows_today = document.getElementById('tvshows_today')
                div_tvshows_today.appendChild(h2_element)

                var table_element = document.createElement('table')
                table_element.className = 'episodes'
                var tbody_element = table_element.createTBody()
                tbody_element.id = 'snippet--episodes {0}'.format(tvshow_name) // should contain name of the episode as ID

                tbody_element.insertAdjacentHTML('afterbegin', todays_episode_element)
                div_tvshows_today.appendChild(table_element)
            }

        }
    }

}

episodesReleasedToday()







