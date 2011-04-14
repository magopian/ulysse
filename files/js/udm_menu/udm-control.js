// UDMv4.52 //
///////////////////////////////////////////////////////////////////
//                                                               //
//  ULTIMATE DROP DOWN MENU Version 4.52 by Brothercake          //
//  http://www.udm4.com/                                         //
//                                                               //
//  This script may not be used or distributed without license   //
//                                                               //
///////////////////////////////////////////////////////////////////



//##########################################################

//*** YOU WILL ALMOST-CERTAINLY NEED TO UPDATE
//*** SERVER-SIDE GENERATORS WHENEVER YOU CHANGE THIS

//##########################################################



//*** DO NOT REMOVE //start or //stop OR SIMILAR COMMENTS


//udm tree global var
var umTree=null;

//ready state flag for popup alignment
//and for shielding unsupported browsers from interactive scripting
//because for them it's never true
um.ready=0;

//cpstart

//parseInt shortcut function
um.pi=function(n){n=parseInt(n,10);return (isNaN(n)?0:n);};

//'undefined'
um.un='undefined';

//document
um.m=document;

//cpstop

//getElementById
um.gd=function(n){return um.m.getElementById(n);};

//make it displayed/non-displayed
um.xd=function(n){n.style.display='block';};
um.xn=function(n){n.style.display='none';};
//make it visible/invisible
um.xv=function(n){n.style.visibility='visible';};
um.xh=function(n){n.style.visibility='hidden';};

//is this a navbar element
um.ne=function(n){return n.parentNode.className=='udm';};

//cpstart

//check for undefined new variables
if(typeof um.reset==um.un){um.reset=['yes','yes','yes'];}
if(typeof um.hstrip==um.un){um.hstrip=['none','yes'];}
//CHANGED
if(typeof um.reset[3]==um.un){um.reset[3]='no';}

//process and copy all custom vars
//both so that we can process them more efficiently
//and so we'll have shortcut-names to reduce the code size

//create an array of custom.js array names
//so we can reference um.something == um['something'] == um[um.cx[i]]
//      0-6           7-9    10-13       14-16    17-48   49-60   61-92
um.cx=['orientation','list','behaviors','navbar','items','menus','menuItems','menuClasses','itemClasses'];

//compact array for custom vars
um.ei=0;um.e=[];

//compact matrix for classes
um.v=[];um.w=[];

//count ad-hoc classes
um.vl=0;
um.wl=0;

//image objects array for caching
um.ek=0;um.im=[];


//process vars method
um.pcv=function(v)
{
	//using regex literals here,because mac/ie5.0
	//appears not to garbage collect the RegExp constructor properly

	//if it's a number variable
	if(v&&/^[+\-]?[0-9]+$/.test(v))
	{
		//turn it into a number
		v=um.pi(v);
		//if this is open or close timer
		//and it's less than 1 set it to 1
		//having a minimum value prevents a potential
		//shadow-displacement problem with popup alignment
		//and also saves a few snips of code in udm-dom.js
		//and also prevents negative numbers
		if((um.ei==10||um.ei==11)&&v<1){v=1;}
	}

	//if it's an image
	if(v&&/\.(gif|png|mng|jpg|jpeg|jpe|bmp)/i.test(v))
	{
		//cache image objects in an array because image loading is asynchronous
		//so it might not have finished before this comes round again
		um.im[um.ek]=new Image;
		um.im[um.ek++].src=um.baseSRC+v;
	}
	return v;
};


//cpstop

//identify dom support//exclude HPR3.04 because its JS capabilities get in the way of good accessibility through graceful degrading
um.d=(typeof um.m.getElementById!=um.un&&(typeof um.m.createElement!=um.un||typeof um.m.createElementNS!=um.un)&&typeof navigator.IBM_HPR==um.un);

//get UA string - used with caution :)
um.u=navigator.userAgent.toLowerCase();

//need to exclude O6,because it declares support for createElement()
//but can't actually add the created element to the page
//this var includes O5 for convenience's sake
um.o5=/opera[\/ ][56]/.test(um.u);
um.k=(navigator.vendor=='KDE');
//CHANGED: if(um.o5||um.k){um.d=0;}
if(um.o5){um.d=0;}

//browsers which support the basic navbar styling
//CHANGED: um.b=(um.d||um.o5||um.k);
um.b=(um.d||um.o5);

//hide static menus for netscape 4 and other primitive CSS browsers
//CHANGED: if(um.list[2]=='yes'&&!(um.d||um.b))
//{
//	document.write('<style type="text/css" media="screen">#udm ul{display:none;}</style>');
//}


//identify specific browsers - these are used to exclude from a feature or add in a hack,
//on the basis that everything is assumed to work right unless it's known not to



//opera 7 or later
um.o7=(um.d&&typeof window.opera!=um.un);
//opera 7.5+ supports clip properly,so clip-based extensions can now be supported
um.o75=0;
//opera 7.3 supports <script> in XHTML
//and hence can't use document.write for generating the CSS rules
//but the alternative methods we're going to use
//fail spectacularly in earlier versions,so we need to distinguish
um.o73=0;
//also need to know about<=7.1,because of a dropshadow positioning problem in 7.0
//it's unlikely anyone will be using 7.0,but it does look terrible,so better to tweak than leave it
//and opera 7.11 dropshadow has lesser,but still unsightly,rendering,sizing and positioning problems
um.o71=0;
if(um.o7)
{
	//CHANGED: split ua string to detect versions
	//um.ov=um.u;
	//um.ov=um.ov.split(/opera[\/ ]7./);
	//um.ov=um.pi(um.ov[1].charAt(0));
	//get major and minor versions from ua string
	um.ova=um.pi(um.u.split(/opera[\/ ]/)[1].match(/[7-9]/)[0]);
	um.ovi=um.pi(um.u.split(/opera[\/ ][7-9]\./)[1].match(/^[0-9]/)[0]);

	//opera 7.5 or later
	//CHANGED: um.o75=(um.ov>=5);
	um.o75=(um.ova>=8||um.ovi>=5);

	//opera 7.3 or later
	//CHANGED: um.o73=(um.ov>=3);
	um.o73=(um.ova>=8||um.ovi>=3);

	//opera 7.1 or earlier
	//CHANGED: um.o71=(um.ov<=1);
	um.o71=(um.ova==7&&um.ovi<=1);
}
//safari
//CHANGED: um.s=(navigator.vendor=='Apple Computer, Inc.'&&typeof um.m.childNodes!=um.un&&typeof um.m.all==um.un&&typeof navigator.taintEnabled==um.un);
//4.52 removed this line:
//um.s=(navigator.vendor=='Apple Computer, Inc.');
//4.52 added these two lines:
um.google=(navigator.vendor=='Google Inc.');
um.s=(navigator.vendor=='Apple Computer, Inc.'||um.google);
//safari 1.2
um.s2=(um.s&&typeof XMLHttpRequest!=um.un);
//4.51 ADDED: safari 3
um.s3=(um.s&&um.u.indexOf('version/3')!=-1);
//4.52 include google in that
um.s3=(um.s3||um.google);
//windows internet explorer
//CHANGED: um.wie=(um.d&&typeof um.m.all!=um.un&&typeof window.opera==um.un);
um.wie=(um.d&&typeof um.m.all!=um.un&&typeof window.opera==um.un&&!um.k);
//mac internet explorer
um.mie=(um.wie&&um.u.indexOf('mac')>0);
//maintain a false OSX/MSN variable, for backward safety
um.mx=0;
um.omie=0;
if(um.mie)
{
	//mac/ie is not win/ie
	um.wie=0;
	//split ua string to detect earlier version
	um.iev=um.u;
	um.iev=um.iev.split('msie ');
	um.iev[1]=um.iev[1].split(';');
	um.iev=parseFloat(um.iev[1][0],10);
	um.omie=(um.iev<5.2);
}
//any version of internet explorer
um.ie=(um.wie||um.mie);
//ie5
um.wie5=(um.wie&&um.u.indexOf('msie 5')>0);
//ie5.5
um.wie55=(um.wie&&um.u.indexOf('msie 5.5')>0);
//ie5.0
um.wie50=(um.wie5&&!um.wie55);
//ie6
um.wie6=(um.wie&&um.u.indexOf('msie 6')>0);
//ie6 is also ie5.5 in these terms
if(um.wie6){um.wie55=1;}
//ie7.0
um.wie7=(um.wie&&typeof XMLHttpRequest!=um.un);

//quirks mode
um.q=(um.wie5||um.mie||((um.wie6||um.wie7||um.o7)&&um.m.compatMode!='CSS1Compat'));
//document.title=um.q;

//***DEV
//alert(''
//	+ 'ie = ' + um.ie + '\n'
//	+ 'wie5 = ' + um.wie5 + '\n'
//	+ 'wie55 = ' + um.wie55 + '\n'
//	+ 'wie50 = ' + um.wie50 + '\n'
//	+ 'wie6 = ' + um.wie6 + '\n'
//	+ 'wie7 = ' + um.wie7 + '\n'
//	+ 'wie8 = ' + um.wie8 + '\n'
//	+ 'quirks = ' + um.q + '\n'
//	);

//gecko earlier than 1.3
um.og=0;
//gecko earlier than 0.9.2
um.dg=0;
//safari spoofs as gecko
if(navigator.product=='Gecko'&&!um.s)
{
	//detect gecko builds by product sub
	um.sub=um.pi(navigator.productSub);
	//gecko<1.3 [tested with 1.3 final]
	um.og=(um.sub<20030312);
	//gecko<1.0.2 [tested with ns7.02]
	um.dg=(um.sub<20030208);
	//win/moz1.0 rc1=Gecko/20020417
	//win/ns7.0=rv:1.0.1) Gecko/20020823
	//win/ns7.02=rv:1.0.2) Gecko/20030208
	//lin/moz1.0.1=20020830
}


//only do the rest for basically support browsers
//this saves unsupported browsers needlessly processing variables
//and also protects MSN TV 2.8 from crash bugs due to (what looks like)
//uses of parseInt and parseFloat,and running the var process code when concatenated!
if(um.b)
{
	//cpstart


	//for each item in the matrix
	var i=0;
	do
	{
		//a normal array
		if(um.cx[i].indexOf('Classes')<0)
		{
			//get array length
			um.cxl=um[um.cx[i]].length;
			//for each item in this array
			var j=0;
			do
			{
				//if array item is not undefined
				//this is for the benefit of opera 5
				//which creates undefined array items from trailing commas
				if(typeof um[um.cx[i]][j]!=um.un)
				{
					//process it
					um.pv=um.pcv(um[um.cx[i]][j]);

					//copy this value
					um.e[um.ei]=um.pv;

					//increment array counter
					um.ei++;
				}
				j++;
			}
			while(j<um.cxl);
		}

		//an ad-hoc class array
		else
		{
			//for each item in this classes array
			for(j in um[um.cx[i]])
			{
				//if member is not a function
				//this is to prevent Array prototypes from being included
				//which might be present in other scripting
				if(typeof um[um.cx[i]][j]!='function')
				{
					//get array length
					um.cxl=um[um.cx[i]][j].length;
					//for each item in this array
					var k=0;
					do
					{
						//if array item is not undefined
						if(typeof um[um.cx[i]][j][k]!=um.un)
						{
							//process it
							um.pcv(um[um.cx[i]][j][k]);
						}
						k++;
					}
					while(k<um.cxl);

					//if this is um.v
					if(um.cx[i]=='menuClasses')
					{
						//copy this array
						um.v[j]=um[um.cx[i]][j];

						//increment matrix counter
						um.vl++;
					}
					//if this is um.w
					else
					{
						//copy this array
						um.w[j]=um[um.cx[i]][j];

						//increment matrix counter
						um.wl++;
					}
				}
			}
		}
		i++;
	}
	while(i<9);


	//cpstop


	//find keyboard module by looking for um.keys    //but some browsers don't support it
	//um.kb=(typeof um.keys!=um.un&&!(um.mie||um.o7||um.s));
	//CHANGED: um.kb=(typeof um.keys!=um.un&&!(um.mie||um.o7||(um.s&&!um.s2)));
	um.kb=(typeof um.keys!=um.un&&!(um.mie||um.o7||um.k||(um.s&&!um.s2)));

	//opera 7.1+ can navigate using spatial navigation,
	//but it doesn't support the hotkey or custom arrow-key navigation
	//because it doesn't allow default-action suppression
	//konqueror 3.2+ also has partial support
	//it can tab navigate the whole structure
	//but it doesn't support the hotkey or custom arrow-key navigation
	//because the event keyCode always comes back as 0
	//CHANGED: um.skb=(um.kb||(typeof um.keys!=um.un&&(um.o7&&!um.o71)));
	um.skb=(um.kb||(typeof um.keys!=um.un&&((um.o7&&!um.o71)||um.k)));


	//find speech module by looking for um.speech // only win/ie supports it
	um.sp=(typeof um.speech!=um.un&&um.wie);

	//when using speech (for all browsers for consistency)
	if(typeof um.speech!=um.un)
	{
		//all menus must open in the same direction
		//and the nav and menus must have the same orientation
		//this makes it easier to use
		//therefore,turn off reposition menus
		//and force the orientation to be vertical
		um.e[12]='no';
		um.e[0]='vertical';
	}


	//cpstart


	//detect relative positioning
	um.rp=(um.e[3]=='relative');



	//cpstop

	//disable reposition menus for win/ie5.0 with relpos v-align navbar
	//because getRealPosition(obj,'y') always returns 0
	if(um.wie50&&um.rp){um.e[12]='no';}


	//cpstart


	//get writing mode from h align variable
	//and set right alignment if it's there
	um.dir='left';
	if(um.e[1]=='rtl'){um.dir='right';um.e[1]='right';}




	//cpstop

	//map old values for windowed control management for backward compatibility
	um.e[13]=(um.e[13]=='yes')?'default':(um.e[13]=='no')?'iframe':um.e[13];


	//detect whether select element hiding is being used
	um.hz=(um.wie50&&um.e[13]=='default')||(um.wie&&um.e[13]=='hide');



	//cpstart


	//detect horizontal navbar
	um.h=um.e[0]=='horizontal';

	//restrict positions to positive values
	i=4;do{if(parseFloat(um.e[i],10)<0){um.e[i]='0';}i++}while(i<6);

	//if rtl text with an h-nav is in use make x an inverse number
	if(um.h&&um.dir=='right'){um.e[4]='-'+um.e[4];}


	//detect popup alignment
	um.p=um.e[0]=='popup';


	//cpstop



	//convert values for popup aligment
	if(um.p)
	{
		um.va=['left','top','absolute','-2000px','-2000px'];
		i=0;do{um.e[i+1]=um.va[i];i++}while(i<5);
		um.e[14]=0;
		um.e[15]=0;
	}


	//CHANGED: detect expanding menus
	um.ep=0;if(um.e[0]=='expanding'){um.ep=1;um.e[0]='vertical';}

	//CHANGED:FT: detect foldertree menus
	//um.ft=0;if(um.e[0]=='foldertree'){um.ep=1;um.ft=1;um.e[0]='vertical';}


	//cpstart

	//store right alignment
	um.a=(um.e[1]=='right');


	//cpstop

	//detect rigid overflow//not supported for RTL text
	um.rg=(um.h&&um.e[7]=='rigid'&&um.dir!='right');


	//cpstart

	//detect position fixed // not supported for IE5-6 or old gecko
	//implement IE5-6 JS equivalent if value is "allfixed"
	//IE7: exclude ie7 from this because it supports true position fixed
	um.fe=false;if(um.e[3]=='allfixed'){um.e[3]='fixed';if(um.wie5||um.wie6){um.fe=true;}}
	um.f=(um.e[3]=='fixed'&&!(um.wie5||um.wie6||um.og));


	//detect active border collapse
	um.nc=(um.e[17]==0&&um.e[19]=='collapse');
	um.mc=(um.e[61]==0&&um.e[63]=='collapse');


	//cpstop


	//no menus for ..
	//	- old gecko builds with relpos
	//	- old mac/ie5 with an h-nav
	//	- ancient gecko or win/ie5.0 with RTL text
	um.nm=((um.og&&um.rp)||(um.omie&&um.h)||((um.dg||um.wie50)&&um.dir=='right'));

	//no arrows for ..
	//	- nomenus group
	//	- mac/ie5
	um.nr=(um.nm||um.mie);

	//no dropshadows for ..
	//	- ancient gecko builds
	//	- opera 7.1 or earlier
	//	- win/ie5.0 with relative positioning
	//	- opera 7 with position:fixed
	//	- mac/ie5
	um.ns=(um.dg||um.o71||(um.wie50&&um.rp)||(um.o7&&um.f)||um.mie);



	//cpstart


	//test support for creating namespaced elements,which allows the script to work within XHTML
	um.cns=(typeof um.m.createElementNS!=um.un);

	//cpstop


	//we also need to use document.styleSheets because document.write won't work
	//IE supports it but uses a proprietary rule syntax
	//that doesn't matter,because IE doesn't support XHTML anyway
	//so we just exclude it by additionally testing for createElementNS
	//safari and konqueror support createElementNS,and they say they supports document.styleSheets
	//but the latter doesn't work properly,so we need to exclude them specifically
	um.ss=(um.cns&&typeof um.m.styleSheets!=um.un&&!(um.s||um.k));

	//4.51 ADDED: Safari 3 supports document.styleSheets properly now
	if(um.s3){um.ss=1;}


	//if keyboard module is in use
	if(um.kb)
	{
		//convert key-handling codes to number
		i=0;do{um.keys[i]=um.pi(um.keys[i]);i++}while(i<5);
		if(um.keys[6]!='none'){um.keys[6]=um.pi(um.keys[6]);}
		else{um.keys[6]=-1;}
	}

	//find arrow images
	//using a regex literal here
	//because mac/ie5.0 doesn't
	//garbage collect the RegExp constructor properly
	um.ni=/(gif|png|mng|jpg|jpeg|jpe|bmp)/i.test(um.e[45]);
	um.mi=/(gif|png|mng|jpg|jpeg|jpe|bmp)/i.test(um.e[89]);


}




//api receivers array
um.rn=0;um.rv=[];

//add to receivers array method
um.addReceiver=function(f,c)
{
	um.rv[um.rn++]=[f,c];
};

//get parent <li> method
um.gp=function(n)
{
	//if input is null,return null
	//if input is a list-item (nodeName converted for O7 in XHTML mode) return it
	//otherwise recur
	return n?um.vn(n.nodeName).toLowerCase()=='li'?n:this.gp(n.parentNode):null;
};


//cpstart

//create element and attributes based on a method by beetle (http://www.peterbailey.net/)
//see http://www.codingforums.com/showthread.php?t=29097 for details
um.createElement=function(n,a)
{
	um.el=(um.cns)?um.m.createElementNS('http://www.w3.org/1999/xhtml',n):um.m.createElement(n);
	if(typeof a!=um.un)
	{
		for(var i in a)
		{
			switch(i)
			{
				case 'text' :
					um.el.appendChild(um.m.createTextNode(a[i]));
					break;
				case 'class' :
					um.el.className=a[i];
					break;
				default :
					um.el.setAttribute(i,'');
					um.el[i]=a[i];
					break;
			}
		}
	}
	return um.el;
};


//cpstop