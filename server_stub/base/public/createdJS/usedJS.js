
function apply(button){
	var heading = button.nextElementSibling;
	var image = button.firstElementChild;
	var hiddenContent = heading.nextElementSibling;
	if( hiddenContent.style.display == 'block' ) {
		image.src="icons/plus-svgrepo-com.svg";
		hiddenContent.style.display = 'none';
	} else {
		image.src="icons/minus-svgrepo-com.svg";
		hiddenContent.style.display = 'block';
	}
}

function applyPurple(button){
	var heading = button.nextElementSibling;
	var image = button.firstElementChild;
	var hiddenContent = heading.nextElementSibling;
	if( hiddenContent.style.display == 'block' ) {
		image.src="icons/plus-svgrepo-comPurple.svg";
		hiddenContent.style.display = 'none';
	} else {
		image.src="icons/minus-svgrepo-comPurple.svg";
		hiddenContent.style.display = 'block';
	}
}


function applyAccordeon(button) {
	
	var headingOfClickedButton = button.nextElementSibling;
	var imageOfClickedButton = button.firstElementChild;
	var hiddenContentOfClickedButton = headingOfClickedButton.nextElementSibling;
	
	var parentClicked, parentOfParent, children, child;
	var actualButton, heading, image,  hiddenContent;
	
		//IF BOX SHOULD BE OPENED, OTHERS MUST BE SCANNED AND CLOSED IF OPEN
	if( hiddenContentOfClickedButton.style.display != 'block' ) {
	
		parentClicked = button.parentElement;
		parentOfParent = parentClicked.parentElement;
		children = parentOfParent.children;
		for(var i=0; i< children.length; i++) {
			child = children[i];
			if( child.tagName == "DIV" && child.classList.contains('expandBox')){
				actualButton = child.firstElementChild;
				heading = actualButton.nextElementSibling;
				image = actualButton.firstElementChild;
				hiddenContent = heading.nextElementSibling;
				if( hiddenContent.style.display == 'block' ) {
					image.src="icons/plus-svgrepo-com.svg";
					hiddenContent.style.display = 'none';
				} 
			}
		}
		imageOfClickedButton.src="icons/minus-svgrepo-com.svg";
		hiddenContentOfClickedButton.style.display = 'block';
	
		//ONLY CLOSE OPENED ONE
	} else {
		imageOfClickedButton.src="icons/plus-svgrepo-com.svg";
		hiddenContentOfClickedButton.style.display = 'none';
	}
}


var observer = new IntersectionObserver(function(entries) {
	// no intersection with screen
	if(entries[0].intersectionRatio === 0)
		document.querySelector("#stickyBar").classList.add("stickyStyle");
	// fully intersects with screen
	else if(entries[0].intersectionRatio === 1)
		document.querySelector("#stickyBar").classList.remove("stickyStyle");
}, { threshold: [0,1] });

observer.observe(document.querySelector("#underSticky"));