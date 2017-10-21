/*********************************************************** 
    On homepage, show episodes which were released today

************************************************************/

// Extending string fucntion
// E.g. '{}'.format(string)
// source code: https://stackoverflow.com/a/25227174
String.prototype.format = function () {
    var args = [].slice.call(arguments);
    return this.replace(/(\{\d+\})/g, function (a){
        return args[+(a.substr(1,a.length-2))||0];
    });
};

// source code: https://stackoverflow.com/a/35130223
function nthParent(element, n) {
    while(n-- && element)  
        element = element.parentNode;
    return element;
}

// Check which episodes were released today and create html elements
// to show them on homepage
function episodesReleasedToday() {

    var today = new Date()
    var dd = today.getDate()
    var mm = today.getMonth()+1

    current_date = dd + '.' + mm + '.'
    console.log("Current date: " + current_date)

    let elements = document.getElementsByTagName("td")
    let arr = [].slice.call(elements)

    // Date format: 5.10., 10.10., 21.10. etc.
    let elementRegex = /(\d){0,2}\.(\d){0,2}\./g;
    
    // arr.forEach(function(element){
    //     elementHtml = element.innerHTML
    //     console.log(elementHtml)
    // });

    // Go through all of the "td" elements in html code (array)
    arr.forEach(function(item) {
        let element = item.innerHTML
        let match = elementRegex.exec(element)

        if (match != null ) {

            // Find the date when episode was released
            var episode_date = match[0]

            // Find class name of TV show which doesnt have any upcoming episodes
            var elementOuter = nthParent(item, 4).className //item.parentNode.parentNode.parentNode.parentNode.className
            var elementID = nthParent(item, 4).id //item.parentNode.parentNode.parentNode.parentNode.className

            if (episode_date == current_date) {

                todays_episode_element = item.parentNode.innerHTML
                todays_episode_node = item.parentNode

                var tvshow_name = todays_episode_node.getElementsByTagName('a').title

                // Hotfix for duplicate elemenets to be skipped. 
                // kinda hacky way, but hey.. it works :-)
                var td_id = 'snippet--episodes {0}'.format(tvshow_name)

                // If episode is already on homepage, continue with forEach loop
                if (todays_episode_node.parentNode.id == td_id) {
                    return;
                }

                // Get name of the TV Show
                var title = nthParent(todays_episode_node, 3).getElementsByTagName('h2')[0].textContent

                // Create html elements for TV shows' episode
                var h2_element = document.createElement('h2')
                var h2_title_node = document.createTextNode(title)
                h2_element.appendChild(h2_title_node)
                var div_tvshows_today = document.getElementById('tvshows_today')
                div_tvshows_today.appendChild(h2_element)
                div_tvshows_today.style.marginBottom = '15%'

                var table_element = document.createElement('table')
                table_element.className = 'episodes'
                var tbody_element = table_element.createTBody()
                tbody_element.id = 'snippet--episodes {0}'.format(tvshow_name) // should contain name of the episode as ID

                tbody_element.insertAdjacentHTML('afterbegin', todays_episode_element)
                div_tvshows_today.appendChild(table_element)
            }
        }
    });

}

episodesReleasedToday()







