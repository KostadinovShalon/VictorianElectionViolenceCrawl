<template>
<v-container>
    <section class="pa-3">
    <v-container >
      <v-form
      ref="form"
      v-model="valid">
        <!-- LINEA 1 -->
       <v-row>
            <v-col sm="3">
              <div class="pl-3 pr-5">
                <v-text-field                  
                  label="Search All Words"
                  required
                  v-model="advancedSearch.searchAllWords"
                  @input="() => onSetSearch(index, advancedSearch)"
                  :rules="keywordRules"
                ></v-text-field>
              </div>
            </v-col>

            <v-col sm="3">
              <div class="pl-3 pr-5">
                <v-text-field                  
                  label="Search Some Words"
                  required
                  v-model="advancedSearch.searchSomeWords"
                  @input="() => onSetSearch(index, advancedSearch)"
                  :rules="keywordRules"
                ></v-text-field>
              </div>
            </v-col>

            <v-col sm="2">
              <div class="pl-3 pr-5">
                <v-text-field                  
                  label="Use Exact Phrase"
                  required
                  v-model="advancedSearch.useExactPhrase"
                  @input="() => onSetSearch(index, advancedSearch)"
                  :rules="keywordRules"
                ></v-text-field>
              </div>
            </v-col>

            <v-col sm="2">
              <div class="pl-3 pr-5">
                <v-text-field                  
                  label="Exclude Words"
                  required
                  v-model="advancedSearch.excludeWords"
                  @input="() => onSetSearch(index, advancedSearch)"
                ></v-text-field>
              </div>
            </v-col>

            <v-col sm="1" md="1" lg="1">
              <div class="pl-3 pr-5">
              <v-checkbox
              outlined
              label="Exact Search"
              @change="() => onSetSearch(index, advancedSearch)"
              v-model="advancedSearch.exactSearch"></v-checkbox>
              </div>
            </v-col>
            <v-col xs="1" md="1" lg="1">
              <div class="pr-7 pt-5">
                <v-btn
                v-if="canBeRemoved"
                text
                icon
                color="error"
                @click="onDelete(index)"
                >
                <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </v-col>
          </v-row>
          <!-- LINEA 2 ------------------------------------------------------------------->
          <v-row>
            <v-col>
              <v-menu
              ref="menuFromDate"
              v-model="menuFromDate"
              :close-on-content-click="false"
              :return-value.sync="advancedSearch.fromDate"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="advancedSearch.fromDate"
                  label="From Date"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  @input="() => onSetSearch(index, advancedSearch)"
                  :rules="fromdateRules"
                  required
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="advancedSearch.fromDate"
                no-title
                scrollable
                :picker-date.sync="pickerDate"
              >
                <v-spacer></v-spacer>
                <v-btn
                  text
                  color="primary"
                  @click="menuFromDate = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="selectFromDate"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
            </v-col>
            <v-col>
              <div class="pr-5">
                <v-menu
              ref="menuToDate"
              v-model="menuToDate"
              :close-on-content-click="false"
              :return-value.sync="advancedSearch.toDate"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="advancedSearch.toDate"
                  label="To Date"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  @input="() => onSetSearch(index, advancedSearch)"
                  :rules="toDateRules"
                  required
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="advancedSearch.toDate"
                no-title
                scrollable
                :picker-date.sync="pickerToDate"
                :min="advancedSearch.fromDate"
              >
                <v-spacer></v-spacer>
                <v-btn
                  text
                  color="primary"
                  @click="menuToDate = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="$refs.menuToDate.save(advancedSearch.toDate)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
              </div>
            </v-col>
           <v-col >
              <div class="pr-5">
                <v-menu
              ref="menuFromAddedDate"
              v-model="menuFromAddedDate"
              :close-on-content-click="false"
              :return-value.sync="advancedSearch.fromDateAddedToSystem"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="advancedSearch.fromDateAddedToSystem"
                  label="From Date Added to System"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  @input="() => onSetSearch(index, advancedSearch)"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="advancedSearch.fromDateAddedToSystem"
                no-title
                scrollable
              >
                <v-spacer></v-spacer>
                <v-btn
                  text
                  color="primary"
                  @click="menuFromAddedDate = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="selectFromAddedDate"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
              </div>
            </v-col>
            <v-col >
              <div class="pr-5">
                <v-menu
              ref="menuToAddedDate"
              v-model="menuToAddedDate"
              :close-on-content-click="false"
              :return-value.sync="advancedSearch.toDateAddedToSystem"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="advancedSearch.toDateAddedToSystem"
                  label="To Date Added to System"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  @input="() => onSetSearch(index, advancedSearch)"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="advancedSearch.toDateAddedToSystem"
                no-title
                scrollable
                :min="advancedSearch.fromDateAddedToSystem"
              >
                <v-spacer></v-spacer>
                <v-btn
                  text
                  color="primary"
                  @click="menuToAddedDate = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="$refs.menuToAddedDate.save(advancedSearch.toDateAddedToSystem)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
              </div>
            </v-col>
          </v-row>
          <!-- LINEA 3 ------------------------------------------------------------------------------------------- -->
          <v-row>
            <v-col sm="3">
              <div class="pr-5">
                <v-autocomplete
                label="Publication Place"
                :items="places"
                v-model="advancedSearch.publicationPlace"
                @change="() => onSetSearch(index, advancedSearch)"
                solo chips
                >
                </v-autocomplete>
              </div>
            </v-col>
            <v-col sm="3">
              <div class="pr-5">
                <v-autocomplete
                label="Newspaper Title"
                :items="newspapers"
                v-model="advancedSearch.newspaperTitle"
                @change="() => onSetSearch(index, advancedSearch)"
                solo chips
                >
                </v-autocomplete>
              </div>
            </v-col>
            <v-col sm="3">
              <v-select
              chips
              label="Article Type"
              :items="articleTypes"
              v-model="advancedSearch.articleType"
              @change="() => onSetSearch(index, advancedSearch)"
              multiple
              solo>
              </v-select>
            </v-col>
            <v-col sm="3">
              <div class="pl-3 pr-5">
                <v-text-field                  
                  label="Tags"
                  required
                  v-model="advancedSearch.tags"
                  @input="() => onSetSearch(index, advancedSearch)"
                ></v-text-field>
              </div>
            </v-col>
          </v-row>
          <!-- LINEA 4 --------------------------------------------------------------------------------------- -->
          <v-row>
            <v-spacer></v-spacer>
            <v-col sm="3" pr="3">
              <v-select
              chips
              label="Sort Results By"
              :items="results"
              @input="() => onSetSearch(index, advancedSearch)"
              v-model="advancedSearch.sortResultsBy"
              solo>
              </v-select>
            </v-col>
            <v-col sm="3" pr="3">
              <v-checkbox
              label="Front Page Articles Only"
              @change="() => onSetSearch(index, advancedSearch)"
              v-model="advancedSearch.frontPageArticlesOnly"></v-checkbox>
            </v-col>
          </v-row>
      </v-form>
    </v-container>
  </section>
  
</v-container>
</template>

<script>
export default {
    //This is the advanced search item that will be called inside AdvancedSearch.vue
    name: 'AdvancedFilter',
    props: {
      onSetSearch: {
        type: Function,
        required: true
      },
      onDelete: Function,
      canBeRemoved: Boolean,
      index: {
        type: Number,
        required: true,
      },
      advancedSearchOriginal: Object,
    },
    computed: {
      advancedSearch() {
        return this.advancedSearchOriginal;
      },
    },
    methods:{
      validate () {
          this.$refs.form.validate()
        },
      selectFromDate(){
        this.$refs.menuFromDate.save(this.advancedSearch.fromDate)
        if(this.advancedSearch.fromDate > this.advancedSearch.toDate){
          this.advancedSearch.toDate = this.advancedSearch.fromDate
        }
      },
      selectFromAddedDate(){
        this.$refs.menuFromAddedDate.save(this.advancedSearch.fromDateAddedToSystem)
        if(this.advancedSearch.fromDateAddedToSystem > this.advancedSearch.toDateAddedToSystem){
          this.advancedSearch.toDateAddedToSystem = this.advancedSearch.fromDateAddedToSystem
        }
      }
    },
    mounted: function(){
      this.pickerDate = '1900-01'
      this.pickerToDate = '1900-01'
    },
    data() {
        return{
            valid: true,
            fromdateRules: [
              v => !!v || 'A starting date is required'
            ],
            toDateRules: [
              v => !!v || 'A end date is required',
              v => v >= this.advancedSearch.fromDate || 'End date must be later thatn start date'
            ],
            keywordRules: [
              () => !!this.advancedSearch.searchAllWords || !!this.advancedSearch.searchSomeWords || !!this.advancedSearch.useExactPhrase || 'At least one field must be present'
            ],
            menuFromDate: false,
            menuToDate: false,
            menuFromAddedDate: false,
            menuToAddedDate: false,
            pickerDate: null,
            pickerToDate: null,
            ranges: ['day', 'week', 'month', 'year'],
            articleTypes: ['Advertisement', 'Article', 'Family notice', 'Ilustrated', 'Miscellaneous'],
            results: ['Relevance', 'Date(oldest)', 'Date(most recent)'],
            newspapers: [
              "Aberdare Times",
              "Aberdeen Evening Express",
              "Aberdeen Free Press",
              "Aberdeen Herald and General Advertiser",
              "Aberdeen People's Journal",
              "Aberdeen Press and Journal",
              "Aberdeen Weekly Free Press",
              "Aberdeen Weekly Journal",
              "Abergavenny Chronicle",
              "Aberystwyth Times",
              "The Advocate: or, Irish Industrial Journal",
              "Alcester Chronicle",
              "Aldershot Military Gazette",
              "Allnut's Irish Land Schedule",
              "Alloa Advertiser",
              "Ally Sloper's Half Holiday",
              "Alnwick Mercury",
              "Ampthill & District News",
              "Annandale Observer and Advertiser",
              "Anti-Slavery Advocate",
              "Arbroath Herald and Advertiser for the Montrose Burghs",
              "Ardrossan and Saltcoats Herald",
              "Aris's Birmingham Gazette",
              "Armagh Guardian",
              "Armagh Standard",
              "Army and Navy Gazette",
              "The Ashton Weekly Reporter, and Stalybridge and Dukinfield Chronicle",
              "Athletic News",
              "Athlone Sentinel",
              "The Atlas",
              "Ayr Advertiser, or, West Country Journal",
              "Ayrshire Express",
              "Ballymena Observer",
              "Ballymena Weekly Telegraph",
              "Ballyshannon Herald",
              "Banbury Advertiser",
              "Banbury Beacon",
              "Banbury Guardian",
              "Baner ac Amserau Cymru",
              "Banffshire Journal and General Advertiser",
              "Banner of Ulster",
              "Barking, East Ham & Ilford Advertiser, Upton Park and Dagenham Gazette",
              "Barnet Press",
              "Barnoldswick & Earby Times",
              "Barnsley Chronicle, etc.",
              "Barnstaple Times and North Devon News",
              "Bath Chronicle and Weekly Gazette",
              "Bath Journal",
              "Bedford Record",
              "Bedfordshire Mercury",
              "Bedfordshire Times and Independent",
              "Belfast Commercial Chronicle",
              "Belfast Mercantile Register and Weekly Advertiser",
              "Belfast Mercury",
              "Belfast Morning News",
              "Belfast News-Letter",
              "Belfast Protestant Journal",
              "Belfast Telegraph",
              "Belfast Weekly News",
              "Bell's Life in London and Sporting Chronicle",
              "Bell's New Weekly Messenger",
              "Bell's Weekly Messenger",
              "Bellshill Speaker",
              "Belper News",
              "Berks and Oxon Advertiser",
              "Berkshire Chronicle",
              "The Berwick Advertiser",
              "Berwickshire News and General Advertiser",
              "Beverley and East Riding Recorder",
              "Beverley Echo",
              "Beverley Guardian",
              "Bexhill-on-Sea Observer",
              "Bexley Heath and Bexley Observer",
              "Bicester Advertiser",
              "Bicester Herald",
              "Biggleswade Chronicle",
              "Birmingham Chronicle",
              "Birmingham Daily Gazette",
              "Birmingham Daily Post",
              "Birmingham Journal",
              "Birmingham Mail",
              "Birmingham Weekly Post",
              "Blackburn Standard",
              "Blackburn Times",
              "Bognor Regis Observer",
              "Bolton Chronicle",
              "Bolton Evening News",
              "Bo'ness Journal, and Linlithgow Advertiser",
              "Boston Guardian",
              "Bournemouth Daily Echo",
              "Bournemouth Graphic",
              "Bournemouth Guardian",
              "Bradford Daily Telegraph",
              "Bradford Observer",
              "Brechin Advertiser",
              "Brechin Herald",
              "Brecon and Radnor Express and Carmarthen Gazette",
              "Brecon Reporter and South Wales General Advertiser",
              "Bridgnorth Journal and South Shropshire Advertiser.",
              "Bridgwater Mercury",
              "Bridlington Free Press",
              "Bridport News",
              "Brighton Gazette",
              "Brighton Guardian",
              "Brighton Herald",
              "Brighton Patriot",
              "Bright's Intelligencer and Arrival List",
              "Bristol Daily Post",
              "Bristol Evening Post",
              "Bristol Magpie",
              "Bristol Mercury",
              "Bristol Mirror",
              "Bristol Times and Mirror",
              "Britannia and Eve",
              "Bromley & District Times",
              "Bromyard News",
              "Broughty Ferry Guide and Advertiser",
              "Buchan Observer and East Aberdeenshire Advertiser",
              "Buckingham Advertiser and Free Press",
              "Buckingham Express",
              "Bucks Advertiser & Aylesbury News",
              "Bucks Chronicle and Bucks Gazette",
              "Bucks Gazette",
              "Bucks Herald",
              "Burnley Advertiser",
              "Burnley Express",
              "Burnley Gazette",
              "Burnley News",
              "Burton Daily Mail",
              "Bury and Norwich Post",
              "Bury Free Press",
              "Bury Times",
              "Buxton Advertiser",
              "Buxton Herald",
              "The Bystander",
              "Caledonian Mercury",
              "Cambrian News",
              "Cambridge Chronicle and Journal",
              "Cambridge Daily News",
              "Cambridge General Advertiser",
              "Cambridge Independent Press",
              "Cambridge Intelligencer",
              "Cambridgeshire Times",
              "Canterbury Journal, Kentish Times and Farmers' Gazette",
              "Cardiff and Merthyr Guardian, Glamorgan, Monmouth, and Brecon Gazette",
              "Cardiff Times",
              "Cardigan & Tivy-side Advertiser",
              "Carlisle Express and Examiner",
              "Carlisle Journal",
              "Carlisle Patriot",
              "Carlow Post",
              "Carluke and Lanark Gazette",
              "Carmarthen Weekly Reporter",
              "Carrickfergus Advertiser",
              "Catholic Standard",
              "Catholic Telegraph",
              "Cavan Observer",
              "The Champion",
              "Chard and Ilminster News",
              "The Charter",
              "Chartist Circular",
              "The Chartist",
              "Chatham News",
              "Chelmsford Chronicle",
              "Chelsea News and General Advertiser",
              "Cheltenham Chronicle",
              "Cheltenham Examiner",
              "Cheltenham Journal and Gloucestershire Fashionable Weekly Gazette.",
              "Cheltenham Looker-On",
              "Cheltenham Mercury",
              "Chepstow Mercury, Volunteers' Gazette, Monmouthshire & South Wales Advertiser",
              "Chepstow Weekly Advertiser",
              "Cheshire Observer",
              "Chester Chronicle",
              "Chester Courant",
              "Chichester Express and West Sussex Journal",
              "Chichester Observer",
              "Chorley Guardian",
              "Chorley Standard and District Advertiser",
              "Christchurch Times",
              "Church League for Women's Suffrage",
              "Cirencester Times and Cotswold Advertiser",
              "Clare Journal, and Ennis Advertiser",
              "Clerkenwell News",
              "Clifton and Redland Free Press",
              "Clifton Society",
              "Clitheroe Advertiser and Times",
              "Clonmel Herald",
              "Cobbett's Weekly Political Register",
              "Colchester Gazette",
              "Coleraine Chronicle",
              "Commercial Journal",
              "Common Cause",
              "Congleton & Macclesfield Mercury, and Cheshire General Advertiser",
              "Connaught Watchman",
              "Conservative and Unionist Women's Franchise Review",
              "Cork Advertising Gazette",
              "Cork Constitution",
              "Cork Examiner",
              "Cornish & Devon Post",
              "The Cornish Telegraph",
              "Cornish Times",
              "Cornishman",
              "Cornubian and Redruth Times",
              "County Advertiser & Herald for Staffordshire and Worcestershire",
              "County Chronicle, Surrey Herald and Weekly Advertiser for Kent",
              "County Courts Chronicle",
              "County Express",
              "County Express; Brierley Hill, Stourbridge, Kidderminster, and Dudley News",
              "Coventry Evening Telegraph",
              "Coventry Herald",
              "Coventry Standard",
              "Coventry Times",
              "Craven Herald",
              "Crawley and District Observer",
              "Crewe Guardian",
              "Cricket and Football Field",
              "Croydon Advertiser and East Surrey Reporter",
              "Croydon Chronicle and East Surrey Advertiser",
              "Croydon Guardian and Surrey County Gazette",
              "Croydon's Weekly Standard",
              "Cumberland & Westmorland Herald",
              "Cumberland and Westmorland Advertiser, and Penrith Literary Chronicle",
              "Cumberland Pacquet, and Ware's Whitehaven Advertiser",
              "Current Prices of Grain at Dublin Corn Exchange",
              "Daily Gazette for Middlesbrough",
              "Daily Herald",
              "Daily Mirror",
              "Daily Record",
              "Daily Telegraph & Courier (London)",
              "Darlington & Stockton Times, Ripon & Richmond Chronicle",
              "Dartmouth & South Hams chronicle",
              "The Days' Doings",
              "Denbighshire Free Press",
              "Derby Daily Telegraph",
              "Derby Mercury",
              "Derbyshire Advertiser and Journal",
              "Derbyshire Courier",
              "Derbyshire Times and Chesterfield Herald",
              "Dereham and Fakenham Times",
              "Derry Journal",
              "Devizes and Wiltshire Gazette",
              "Dewsbury Reporter",
              "Diss Express",
              "Doncaster Gazette",
              "Donegal Independent",
              "Dorchester and Sherborne journal, and Western Advertiser",
              "Dorking and Leatherhead Advertiser",
              "Dorset County Chronicle",
              "Dover Express",
              "Dover Telegraph and Cinque Ports General Advertiser",
              "Downpatrick Recorder",
              "Downshire Protestant",
              "Driffield Times",
              "Drogheda Argus and Leinster Journal",
              "Drogheda Conservative Journal",
              "Drogheda Journal, or Meath & Louth Advertiser",
              "Drogheda News Letter",
              "The Dublin Builder",
              "Dublin Correspondent",
              "Dublin Courier",
              "Dublin Daily Express",
              "Dublin Daily Nation",
              "Dublin Evening Mail",
              "Dublin Evening Packet and Correspondent",
              "Dublin Evening Post",
              "Dublin Evening Telegraph",
              "Dublin Intelligence",
              "Dublin Medical Press",
              "Dublin Mercantile Advertiser, and Weekly Price Current",
              "Dublin Monitor",
              "Dublin Morning Register",
              "Dublin Observer",
              "Dublin Shipping and Mercantile Gazette",
              "Dublin Weekly Herald",
              "Dublin Weekly Nation",
              "Dublin Weekly Register",
              "Dudley and District News",
              "Dudley Guardian, Tipton, Oldbury & West Bromwich Journal and District Advertiser",
              "Dudley Herald",
              "Dudley Mercury, Stourbridge, Brierley Hill, and County Express",
              "Dumfries and Galloway Standard",
              "Dundalk Democrat, and People's Journal",
              "Dundalk Examiner and Louth Advertiser.",
              "Dundee Advertiser",
              "Dundee Courier",
              "Dundee Evening Post",
              "Dundee Evening Telegraph",
              "Dundee People's Journal",
              "Dundee Weekly News",
              "The Dundee Year Book",
              "Dundee, Perth, and Cupar Advertiser",
              "Dunfermline Press",
              "Dunfermline Saturday Press",
              "Dunstable Chronicle, and Advertiser for Beds, Bucks & Herts",
              "Durham Chronicle",
              "Durham County Advertiser",
              "East & South Devon Advertiser.",
              "East Anglian Daily Times",
              "East Kent Times",
              "East London Observer",
              "East Suffolk Mercury and Lowestoft Weekly News",
              "Eastbourne Gazette",
              "Eastbourne Herald",
              "Eastern Daily Press",
              "Eastern Evening News",
              "Eastern Morning News",
              "Eddowes's Journal, and General Advertiser for Shropshire, and the Principality of Wales",
              "Edinburgh Courant",
              "Edinburgh Evening Courant",
              "Edinburgh Evening News",
              "Edinburgh Evening Post and Scottish Standard",
              "Elgin Courant, and Morayshire Advertiser",
              "Elgin Courier",
              "English Lakes Visitor",
              "The Enniscorthy News, and County of Wexford Advertiser.",
              "Enniskillen Chronicle and Erne Packet",
              "Epworth Bells, Crowle and Isle of Axholme Messenger",
              "The Era",
              "Essex Herald",
              "Essex Newsman",
              "Essex Standard",
              "The Evening Chronicle",
              "Evening Despatch",
              "The Evening Freeman.",
              "Evening Herald (Dublin)",
              "Evening Mail",
              "Evening Star",
              "Evesham Journal",
              "The Examiner",
              "Exeter and Plymouth Gazette",
              "Exeter and Plymouth Gazette Daily Telegrams",
              "Exeter Flying Post",
              "Exmouth Journal",
              "Express and Echo",
              "Falkirk Herald",
              "Falmouth Express and Colonial Journal",
              "Faringdon Advertiser and Vale of the White Horse Gazette",
              "Farmer's Gazette and Journal of Practical Horticulture",
              "Faversham Gazette, and Whitstable, Sittingbourne, & Milton Journal",
              "Faversham Times and Mercury and North-East Kent Journal",
              "Fife Free Press, & Kirkcaldy Guardian",
              "Fife Herald",
              "Fifeshire Advertiser",
              "Flag of Ireland",
              "Folkestone, Hythe, Sandgate & Cheriton Herald",
              "Forfar Dispatch",
              "Forres Elgin and Nairn Gazette, Northern Review and Advertiser",
              "Framlingham Weekly News",
              "Fraserburgh Herald and Northern Counties' Advertiser",
              "Free Church Suffrage Times",
              "Freeman's Journal",
              "Frome Times",
              "Fulham Chronicle",
              "Galloway Advertiser and Wigtownshire Free Press.",
              "Galloway Express",
              "Galloway Gazette",
              "Galway Mercury, and Connaught Weekly Advertiser",
              "Galway Patriot",
              "Galway Vindicator, and Connaught Advertiser",
              "General Advertiser for Dublin, and all Ireland",
              "Glamorgan Free Press",
              "Glasgow Citizen",
              "Glasgow Constitutional",
              "Glasgow Courant",
              "Glasgow Evening Citizen",
              "Glasgow Evening Post",
              "Glasgow Free Press",
              "Glasgow Gazette",
              "Glasgow Herald",
              "Glasgow Morning Journal",
              "Glasgow Saturday Post, and Paisley and Renfrewshire Reformer",
              "Glasgow Sentinel",
              "Globe",
              "Glossop Record",
              "Glossop-dale Chronicle and North Derbyshire Reporter",
              "Gloucester Citizen",
              "Gloucester Journal",
              "Gloucestershire Chronicle",
              "Gloucestershire Echo",
              "Good Morning",
              "Goole Times",
              "Gore's Liverpool General Advertiser",
              "Grantham Journal",
              "Graphic",
              "The Graphic",
              "Gravesend Reporter, North Kent and South Essex Advertiser",
              "Grays & Tilbury Gazette, and Southend Telegraph",
              "Greenock Advertiser",
              "Greenock Telegraph and Clyde Shipping Gazette",
              "Grimsby Daily Telegraph",
              "Hackney and Kingsland Gazette",
              "Haddingtonshire Courier",
              "The Halesworth Times and East Suffolk Advertiser.",
              "Halifax Courier",
              "Hamilton Advertiser",
              "Hamilton Herald and Lanarkshire Weekly News",
              "Hampshire Advertiser",
              "Hampshire Chronicle",
              "Hampshire Telegraph",
              "Hampstead & Highgate Express",
              "Hants and Berks Gazette and Middlesex and Surrey Journal",
              "Harrogate Herald",
              "Hartland and West Country Chronicle",
              "Hartlepool Free Press and General Advertiser",
              "Hartlepool Northern Daily Mail",
              "Hastings and St Leonards Observer",
              "Hawick News and Border Chronicle",
              "Hemel Hempstead Gazette and West Herts Advertiser",
              "Hendon & Finchley Times",
              "Henley & South Oxford Standard",
              "Henley Advertiser",
              "Hereford Journal",
              "Hereford Times",
              "Hertford Mercury and Reformer",
              "Hertfordshire Express and General Advertiser",
              "Herts & Cambs Reporter & Royston Crow",
              "Herts Advertiser",
              "Herts Guardian, Agricultural Journal, and General Advertiser",
              "Hexham Courant",
              "Hibernian Journal; or, Chronicle of Liberty",
              "Highland Sentinel",
              "Holborn Journal",
              "Homeward Mail from India, China and the East",
              "Horfield and Bishopston Record and Montepelier & District Free Press",
              "Horncastle News",
              "Horsham, Petworth, Midhurst and Steyning Express",
              "Huddersfield and Holmfirth Examiner",
              "Huddersfield Chronicle",
              "Huddersfield Daily Examiner",
              "Hull Advertiser and Exchange Gazette",
              "Hull and Eastern Counties Herald",
              "Hull Daily Mail",
              "Hull Packet",
              "Huntingdon, Bedford & Peterborough Gazette",
              "Hunts Post",
              "Hyde & Glossop Weekly News, and North Cheshire Herald",
              "Ilford Recorder",
              "Ilkeston Pioneer",
              "Ilkley Gazette and Wharfedale Advertiser",
              "Illustrated Advertiser of the Royal Dublin Society",
              "Illustrated Berwick Journal",
              "Illustrated London News",
              "Illustrated Malvern Advertiser, Visitors' List, and General Weekly Newspaper",
              "Illustrated Police Budget",
              "Illustrated Police News",
              "Illustrated Sporting and Dramatic News",
              "Illustrated Times",
              "Illustrated War News",
              "Illustrated Weekly News",
              "International Woman Suffrage News",
              "Inverness Courier",
              "Ipswich Advertiser, or, Illustrated Monthly Miscellany",
              "Ipswich Journal",
              "The Ipswich Journal",
              "Irish Citizen",
              "Irish Ecclesiastical Gazette",
              "Irish Independent",
              "Irish News and Belfast Morning News",
              "The Irish Racing Book and Sheet Calendar",
              "Irish Society (Dublin)",
              "Irish Times",
              "The Irishman",
              "Isle of Man Daily Times",
              "Isle of Man Times",
              "Isle of Wight County Press and South of England Reporter",
              "Isle of Wight Mercury",
              "Isle of Wight Observer",
              "Isle of Wight Times",
              "Islington Gazette",
              "Jarrow Express",
              "Jedburgh Gazette",
              "Jersey Independent and Daily Telegraph",
              "John Bull",
              "John o' Groat Journal",
              "Journal of the Chemico-Agricultural Society of Ulster and Record of Agriculture and Industry",
              "Keighley News",
              "Kelso Chronicle",
              "Kendal Mercury",
              "Kent & Sussex Courier",
              "Kentish Chronicle",
              "Kentish Gazette",
              "Kentish Independent",
              "Kentish Mercury",
              "Kentish Weekly Post or Canterbury Journal",
              "Kerry Evening Post.",
              "Kerry Examiner and Munster General Observer",
              "Kidderminster Times and Advertiser for Bewdley & Stourport",
              "Kilburn Times",
              "Kildare Observer and Eastern Counties Advertiser",
              "Kilkenny Journal, and Leinster Commercial and Literary Advertiser",
              "Kilsyth Chronicle",
              "Kings County Chronicle",
              "Kinross-shire Advertiser.",
              "Kirkintilloch Gazette",
              "Kirkintilloch Herald",
              "Knaresborough Post",
              "Lakes Chronicle and Reporter",
              "Lake's Falmouth Packet and Cornwall Advertiser",
              "Lakes Herald",
              "Lambeth and Southwark Advertiser",
              "Lanarkshire Upper Ward Examiner",
              "Lancashire Evening Post",
              "Lancaster Gazette",
              "Lancaster Guardian",
              "Larne Times",
              "Launceston Weekly News, and Cornwall & Devon Advertiser.",
              "Leamington Advertiser, and Beck's List of Visitors",
              "Leamington Spa Courier",
              "Leamington, Warwick, Kenilworth & District Daily Circular",
              "Leeds Intelligencer",
              "Leeds Mercury",
              "Leeds Patriot and Yorkshire Advertiser",
              "Leeds Times",
              "Leek Post & Times and Cheadle News & Times and Moorland Advertiser",
              "Leicester Chronicle",
              "Leicester Daily Mercury",
              "Leicester Daily Post",
              "Leicester Guardian",
              "Leicester Herald",
              "Leicester Journal",
              "Leicester Mail",
              "Leicestershire Mercury",
              "Leigh Chronicle and Weekly District Advertiser",
              "Leigh Journal and Times",
              "Leighton Buzzard Observer and Linslade Gazette",
              "Leinster Independent",
              "Leinster Leader",
              "Leitrim Advertiser",
              "Leominster News and North West Herefordshire & Radnorshire Advertiser",
              "Lichfield Mercury",
              "Limerick and Clare Examiner",
              "Limerick Chronicle",
              "Limerick Evening Post",
              "Limerick Reporter",
              "Lincoln Gazette.",
              "Lincolnshire Chronicle",
              "Lincolnshire Echo",
              "Lincolnshire Free Press",
              "Lincolnshire Standard and Boston Guardian",
              "Linlithgowshire Gazette",
              "Lisburn Herald, and Antrim and Down Advertiser",
              "Littlehampton Gazette",
              "Liverpool Courier and Commercial Advertiser",
              "Liverpool Daily Post",
              "Liverpool Echo",
              "Liverpool Evening Express",
              "Liverpool Mail",
              "Liverpool Mercury",
              "Llandudno Register and Herald",
              "Lloyd's List",
              "Lloyd's Weekly Newspaper",
              "London and Provincial Entr'acte",
              "London City Press",
              "London Courier and Evening Gazette",
              "London Daily News",
              "London Dispatch",
              "London Evening Standard",
              "Londonderry Sentinel",
              "Londonderry Standard",
              "Longford Journal",
              "Loughborough Echo",
              "Loughborough Monitor",
              "Louth and North Lincolnshire Advertiser",
              "Lowestoft Journal",
              "Ludlow Advertiser",
              "Lurgan Mail",
              "Luton News and Bedfordshire Chronicle",
              "Luton Reporter",
              "Luton Times and Advertiser",
              "Luton Weekly Recorder",
              "Macclesfield Courier and Herald, Congleton Gazette, Stockport Express, and Cheshire General Advertiser.",
              "Maidstone Journal and Kentish Advertiser",
              "Maidstone Telegraph",
              "Man of Ross, and General Advertiser",
              "Manchester Courier and Lancashire General Advertiser",
              "Manchester Evening News",
              "Manchester Mercury",
              "Manchester Times",
              "Mansfield Reporter",
              "Market Harborough Advertiser and Midland Mail",
              "Market Rasen Weekly Mail, and Lincolnshire Advertiser",
              "Marylebone Mercury",
              "Maryport Advertiser",
              "Mayo Constitution",
              "Meath People, and Cavan and Westmeath Chronicle",
              "Melton Mowbray Mercury and Oakham and Uppingham News",
              "Merthyr Telegraph, and General Advertiser for the Iron Districts of South Wales",
              "Merthyr Times, and Dowlais Times, and Aberdare Echo",
              "Mid Sussex Times",
              "Middlesex & Surrey Express",
              "Middlesex Chronicle",
              "Midland Examiner and Times",
              "Mid-Ulster Mail",
              "Military Register",
              "Millom Gazette",
              "Milngavie and Bearsden Herald",
              "Missionary Herald of the Presbyterian Church in Ireland",
              "Monitor, and Missionary Chronicle, of the Reformed Presbyterian Church in Ireland",
              "Monmouthshire Beacon",
              "Monmouthshire Merlin",
              "Montgomery County Times and Shropshire and Mid-Wales Advertiser",
              "Montgomeryshire Echo",
              "Montgomeryshire Express",
              "Montrose, Arbroath and Brechin review; and Forfar and Kincardineshire advertiser.",
              "Morecambe Guardian",
              "Morning Advertiser",
              "Morning Chronicle",
              "Morning Post",
              "Morpeth Herald",
              "Mothers' Companion",
              "Motherwell Times",
              "The Munster express, or, weekly commercial & agricultural gazette.",
              "Music Hall and Theatre Review",
              "Nairnshire Mirror, and General Advertiser",
              "Nairnshire Telegraph and General Advertiser for the Northern Counties",
              "Nantwich Guardian",
              "National Teacher, and Irish Educational Journal (Dublin, Ireland)",
              "Naval & Military Gazette and Weekly Chronicle of the United Service",
              "Nelson Leader",
              "Newbury Weekly News and General Advertiser",
              "Newcastle Chronicle",
              "Newcastle Courant",
              "Newcastle Daily Chronicle",
              "Newcastle Evening Chronicle",
              "Newcastle Guardian and Tyne Mercury",
              "Newcastle Journal",
              "Newry Examiner and Louth Advertiser",
              "Newry Herald and Down, Armagh, and Louth Journal",
              "Newry Reporter",
              "Newry Telegraph",
              "Norfolk Chronicle",
              "Norfolk News",
              "North & South Shields Gazette and Northumberland and Durham Advertiser",
              "North Devon Gazette",
              "North Devon Journal",
              "North London News",
              "North Star and Farmers' Chronicle",
              "North Wales Chronicle",
              "North Wales Times",
              "Northampton Chronicle and Echo",
              "Northampton Mercury",
              "Northants Evening Telegraph",
              "Northern Constitution",
              "Northern Daily Telegraph",
              "Northern Echo",
              "Northern Liberator",
              "Northern Standard",
              "Northern Star and Leeds General Advertiser",
              "Northern times and weekly journal for Sutherland and the North",
              "Northern Warder and General Advertiser for the Counties of Fife, Perth and Forfar",
              "Northern Whig",
              "Northwich Guardian",
              "Norwich Mercury",
              "Norwood News",
              "Nottingham Evening Post",
              "Nottingham Gazette, and Political, Literary, Agricultural & Commercial Register for the Midland Counties.",
              "Nottingham Journal",
              "Nottingham Review and General Advertiser for the Midland Counties",
              "Nottinghamshire Guardian",
              "Nuneaton Advertiser",
              "Oban Times, and Argyllshire Advertiser",
              "The Odd Fellow",
              "The Operative",
              "Orkney Herald, and Weekly Advertiser and Gazette for the Orkney & Zetland Islands",
              "Ormskirk Advertiser",
              "Ossett Observer",
              "Oswestry Advertiser",
              "Oxford Chronicle and Reading Gazette",
              "Oxford Journal",
              "Oxford Times",
              "Oxford University and City Herald",
              "Oxfordshire Telegraph",
              "Oxfordshire Weekly News",
              "Paisley & Renfrewshire Gazette",
              "Paisley Daily Express",
              "Paisley Herald and Renfrewshire Advertiser",
              "Pall Mall Gazette",
              "Pateley Bridge & Nidderdale Herald",
              "Pearson's Weekly",
              "Peeblesshire Advertiser",
              "Penarth Chronicle and Cogan Echo",
              "Penny Despatch and Irish Weekly Newspaper",
              "Penny Illustrated Paper",
              "Penrith Observer",
              "The People",
              "Perry's Bankrupt Gazette",
              "Perthshire Advertiser",
              "Perthshire Courier",
              "Peterborough Advertiser",
              "Peterhead Sentinel and General Advertiser for Buchan District",
              "Petersfield Express",
              "Pierce Egan's Weekly Courier",
              "The Pilot",
              "Plymouth and Devonport Weekly Journal and General Advertiser for Devon, Cornwall, Somerset and Dorset.",
              "Police Gazette",
              "Pontefract Advertiser",
              "Pontypool Free Press",
              "Poor Law Unions' Gazette",
              "Poor Man's Guardian",
              "Portadown Times",
              "Portobello Advertiser",
              "Portsmouth Evening News",
              "Portsmouth Times and Naval Gazette",
              "Potter's Electric News",
              "Prescot Reporter, and St. Helens General Advertiser",
              "Preston Chronicle",
              "Preston Herald",
              "The Principality",
              "Public Ledger and Daily Advertiser",
              "Pue's Occurrences",
              "Reading Mercury",
              "Reading Observer",
              "The Referee",
              "Reynolds's Newspaper",
              "Rhyl Journal",
              "Rhyl Record and Advertiser",
              "Ripley and Heanor News and Ilkeston Division Free Press",
              "Rochdale Observer",
              "Rochdale Pilot, and General Advertiser",
              "Rochester, Chatham & Gillingham Journal",
              "Roscommon & Leitrim Gazette",
              "Roscommon Journal, and Western Impartial Reporter",
              "Roscommon Messenger",
              "Ross Gazette",
              "Ross-shire Journal",
              "Rothesay Chronicle",
              "Royal Cornwall Gazette",
              "Royal Devonport Telegraph, and Plymouth Chronicle",
              "Rugby Advertiser",
              "Rutland Echo and Leicestershire Advertiser",
              "Saffron Walden Weekly News",
              "Salisbury and Winchester Journal",
              "The Salisbury Times",
              "Salopian Journal",
              "Saunders's News-Letter",
              "Scarborough Mercury",
              "The Scots Magazine",
              "The Scotsman",
              "Scottish Banner",
              "Scottish Guardian, Glasgow",
              "Scottish Referee",
              "Scunthorpe Evening Telegraph",
              "Sevenoaks Chronicle and Kentish Advertiser",
              "Sheffield Daily News, and Morning Advertiser",
              "Sheffield Daily Telegraph",
              "Sheffield Evening Telegraph",
              "Sheffield Independent",
              "Sheffield Iris",
              "Sheffield Register, Yorkshire, Derbyshire, & Nottinghamshire Universal Advertiser",
              "Sheffield Weekly Telegraph",
              "Shepton Mallet Journal",
              "Sherborne Journal",
              "Sherborne Mercury",
              "Shetland Times",
              "Shields Daily Gazette",
              "Shields Daily News",
              "Shipley Times and Express",
              "Shipping and Mercantile Gazette",
              "Shoreditch Observer",
              "Shrewsbury Chronicle",
              "Shrewsbury Free Press, and Advertiser for Salop",
              "Sidmouth Journal and Directory",
              "Silurian, Cardiff, Merthyr, and Brecon Mercury, and South Wales General Advertiser",
              "Skegness Standard",
              "The Sketch",
              "Skibbereen & West Carbery Eagle; or, South Western Advertiser",
              "Sligo Champion",
              "Sligo Journal",
              "Sligo Observer",
              "The Social Review (Dublin, Ireland : 1893)",
              "Somerset County Gazette",
              "Soulby's Ulverston Advertiser and General Intelligencer",
              "South Bucks Free Press, Wycombe and Maidenhead Journal",
              "South Bucks Standard",
              "South Durham & Cleveland Mercury",
              "South Eastern Gazette",
              "South London Chronicle",
              "South London Press",
              "South Wales Daily News",
              "South Wales Daily Post",
              "South Wales Echo",
              "South Wales Star",
              "Southend Standard and Essex Weekly Advertiser",
              "Southern Echo",
              "Southern Reporter",
              "Southern Reporter and Cork Commercial Courier",
              "Southern Star",
              "Southern Times and Dorset County Herald",
              "Southport Independent and Ormskirk Chronicle",
              "The Sphere",
              "Sporting Life",
              "Sporting Times",
              "Sports Argus",
              "The Sportsman",
              "St James's Gazette",
              "St. Andrews Citizen",
              "St. Neots Chronicle and Advertiser",
              "Staffordshire Advertiser",
              "Staffordshire Chronicle",
              "Staffordshire Gazette and County Standard",
              "Staffordshire Sentinel",
              "Staffordshire Sentinel and Commercial & General Advertiser",
              "The Stage",
              "Stamford Mercury",
              "Star Green 'un",
              "The Star",
              "Statesman and Dublin Christian Record",
              "Stirling Observer",
              "Stockport Advertiser and Guardian",
              "Stonehaven Journal",
              "Stornoway Gazette and West Coast Advertiser",
              "Stroud Journal",
              "Stroud News and Gloucestershire Advertiser",
              "Suffolk and Essex Free Press",
              "The Suffolk Chronicle; or Weekly General Advertiser & County Express.",
              "The Suffragette",
              "Suffragist",
              "Sunday Mirror",
              "Sunday Post",
              "Sunday Sun (Newcastle)",
              "Sunday Times",
              "Sunderland Daily Echo and Shipping Gazette",
              "Surrey Advertiser",
              "Surrey Comet",
              "Surrey Gazette",
              "Surrey Mirror",
              "Sussex Advertiser",
              "Sussex Agricultural Express",
              "Swindon Advertiser and North Wilts Chronicle",
              "Tadcaster Post, and General Advertiser for Grimstone",
              "Tamworth Herald",
              "The Tatler",
              "Taunton Courier, and Western Advertiser",
              "Teesdale Mercury",
              "Tenbury Wells Advertiser",
              "Tenby Observer",
              "The Tewkesbury Register, and Agricultural Gazette.",
              "Thame Gazette",
              "Thanet Advertiser",
              "Thetford & Watton Times and People's Weekly Journal.",
              "Tipperary Free Press",
              "Tipperary Vindicator",
              "Tiverton Gazette (Mid-Devon Gazette)",
              "Todmorden & District News",
              "Todmorden Advertiser and Hebden Bridge Newsletter",
              "Torbay Express and South Devon Echo",
              "Torquay Directory and South Devon Journal",
              "Torquay Times, and South Devon Advertiser",
              "Totnes Weekly Times",
              "Tower Hamlets Independent and East End Local Advertiser",
              "Tralee Chronicle",
              "Tuam Herald",
              "Tyne Mercury; Northumberland and Durham and Cumberland Gazette",
              "Tyrone Constitution",
              "Tyrone Courier",
              "Ulster Gazette",
              "Ulster General Advertiser, Herald of Business and General Information",
              "The Ulsterman",
              "Ulverston Mirror and Furness Reflector",
              "United Irishman",
              "Usk Observer, Raglan Herald, and Monmouthshire Central Advertiser",
              "Uxbridge & W. Drayton Gazette",
              "Vindicator",
              "Volunteer Service Gazette and Military Dispatch",
              "Vote",
              "Votes for Women",
              "Walsall Advertiser",
              "Walsall Free Press and General Advertiser",
              "Walsall Observer, and South Staffordshire Chronicle",
              "Waltham Abbey and Cheshunt Weekly Telegraph",
              "Warder and Dublin Weekly Mail",
              "Warminster & Westbury journal, and Wilts County Advertiser",
              "Warminster Miscellany, and Local Advertiser",
              "Warrington Guardian",
              "Warwick and Warwickshire Advertiser",
              "Waterford Chronicle",
              "Waterford Mail",
              "Waterford Mirror and Tramore Visitor.",
              "Waterford News",
              "Waterford Standard",
              "Watford Observer",
              "Weekly Casualty List (War Office & Air Ministry )",
              "Weekly Freeman's Journal",
              "Weekly Gazette, Incumbered Estates Record & National Advertiser (Dublin, Ireland)",
              "Weekly Irish Times",
              "Weekly Vindicator",
              "Wellington Journal",
              "Wells Journal",
              "West Briton and Cornwall Advertiser",
              "West Cumberland Times",
              "West Kent Guardian",
              "West London Observer",
              "West Middlesex Advertiser and Family Journal",
              "West Middlesex Herald",
              "West Somerset Free Press",
              "West Surrey Times",
              "West Sussex County Times",
              "West Sussex Gazette",
              "Western Chronicle",
              "Western Courier, West of England Conservative, Plymouth and Devonport Advertiser",
              "Western Daily Mercury.",
              "Western Daily Press",
              "Western Gazette",
              "Western Mail",
              "Western Morning News",
              "Western Times",
              "Westmeath Independent",
              "Westmeath Journal",
              "Westmorland Advertiser and Kendal Chronicle",
              "Westmorland Gazette",
              "Weston Mercury",
              "Weston-super-Mare Gazette, and General Advertiser",
              "Wetherby News, and Central Yorkshire Journal",
              "Wexford Conservative",
              "Wexford Constitution",
              "Wexford Independent",
              "Wharfedale & Airedale Observer",
              "Whitby Gazette",
              "Whitby Times, and North Yorkshire Advertiser",
              "Whitchurch Herald",
              "Whitehaven News",
              "Whitstable Times and Herne Bay Herald",
              "Wicklow News-Letter and County Advertiser",
              "Wicklow People",
              "Wigan Observer and District Advertiser",
              "Wigton Advertiser",
              "Willesden Chronicle",
              "Wilts and Gloucestershire Standard",
              "Wiltshire Independent",
              "Wiltshire Times and Trowbridge Advertiser",
              "Windsor and Eton Express",
              "Winsford & Middlewich Guardian",
              "Wisbech Chronicle, General Advertiser and Lynn News",
              "Wisbech Standard",
              "Witney Express and Oxfordshire and Midland Counties Herald",
              "Witney Gazette and West Oxfordshire Advertiser",
              "Wolverhampton Chronicle and Staffordshire Advertiser",
              "Woman's Dreadnought",
              "Woman's Signal",
              "Women's Franchise",
              "Women's Suffrage",
              "Women's Suffrage Record",
              "Woolwich Gazette",
              "Worcester Herald",
              "Worcester Journal",
              "Worcestershire Chronicle",
              "Workington Star",
              "Worthing Gazette",
              "Worthing Herald",
              "Wrexham Advertiser",
              "Wrexham Guardian and Denbighshire and Flintshire Advertiser",
              "Wrexhamite and Denbighshire and Flintshire Reporter",
              "Y Genedl Gymreig",
              "Y Goleuad",
              "Yarmouth Independent",
              "Yarmouth Mercury",
              "York Herald",
              "Yorkshire Early Bird",
              "Yorkshire Evening Post",
              "Yorkshire Evening Press",
              "Yorkshire Gazette",
              "Yorkshire Post and Leeds Intelligencer",
              "Young Woman"],
            places: [
              "Aberdare, Glamorgan, Wales",
              "Aberdeen, Aberdeenshire, Scotland",
              "Abergavenny, Monmouthshire, Wales",
              "Aberystwyth, Cardiganshire, Wales",
              "Alcester, Warwickshire, England",
              "Aldershot, Hampshire, England",
              "Alloa, Clackmannanshire, Scotland",
              "Alnwick, Northumberland, England",
              "Ambleside, Westmorland, England",
              "Ampthill, Bedfordshire, England",
              "Annan, Dumfriesshire, Scotland",
              "Arbroath, Angus, Scotland",
              "Ardrossan, Ayrshire, Scotland",
              "Armagh, Armagh, Northern Ireland",
              "Arundel, Sussex, England",
              "Ashton-under-Lyne, Lancashire, England",
              "Athlone, Westmeath, Republic of Ireland",
              "Aylesbury, Buckinghamshire, England",
              "Ayr, Ayrshire, Scotland",
              "Ballina, Mayo, Republic of Ireland",
              "Ballymena, Antrim, Northern Ireland",
              "Ballyshannon, Donegal, Republic of Ireland",
              "Banbury, Oxfordshire, England",
              "Banff, Banffshire, Scotland",
              "Bangor, Caernarfonshire, Wales",
              "Barnard Castle, Durham, England",
              "Barnoldswick, Yorkshire, England",
              "Barnsley, Yorkshire, England",
              "Barnstaple, Devon, England",
              "Barry, Glamorgan, Wales",
              "Basingstoke, Hampshire, England",
              "Bath, Somerset, England",
              "Bedford, Bedfordshire, England",
              "Belfast, Antrim, Northern Ireland",
              "Bellshill, Lanarkshire, Scotland",
              "Belper, Derbyshire, England",
              "Berwick-upon-Tweed, Northumberland, England",
              "Beverley, Yorkshire, England",
              "Bexhill, Sussex, England",
              "Bicester, Oxfordshire, England",
              "Bideford, Devon, England",
              "Biggleswade, Bedfordshire, England",
              "Birmingham, Warwickshire, England",
              "Blackburn, Lancashire, England",
              "Bognor Regis, Sussex, England",
              "Bolton, Lancashire, England",
              "Boston, Lincolnshire, England",
              "Bournemouth, Hampshire, England",
              "Boyle, Roscommon, Republic of Ireland",
              "Bradford, Yorkshire, England",
              "Brechin, Angus, Scotland",
              "Brecon, Brecknockshire, Wales",
              "Bridgnorth, Shropshire, England",
              "Bridgwater, Somerset, England",
              "Bridlington, Yorkshire, England",
              "Bridport, Dorset, England",
              "Brierley Hill, Staffordshire, England",
              "Brighton, Sussex, England",
              "Bristol, Bristol, England",
              "Bromley, Kent, England",
              "Bromyard, Herefordshire, England",
              "Buckingham, Buckinghamshire, England",
              "Burnley, Lancashire, England",
              "Burton upon Trent, Staffordshire, England",
              "Bury St Edmunds, Suffolk, England",
              "Bury, Lancashire, England",
              "Buxton, Derbyshire, England",
              "Caernarvon, Caernarfonshire, Wales",
              "Cambridge, Cambridgeshire, England",
              "Canterbury, Kent, England",
              "Cardiff, Glamorgan, Wales",
              "Cardigan, Cardiganshire, Wales",
              "Carlisle, Cumberland, England",
              "Carlow, Carlow, Republic of Ireland",
              "Carluke, Lanarkshire, Scotland",
              "Carmarthen, Carmarthenshire, Wales",
              "Carrickfergus, Antrim, Northern Ireland",
              "Castle Douglas, Kirkcudbrightshire, Scotland",
              "Castlebar, Mayo, Republic of Ireland",
              "Cavan, Cavan, Republic of Ireland",
              "Chard, Somerset, England",
              "Chatham, Kent, England",
              "Chelmsford, Essex, England",
              "Cheltenham, Gloucestershire, England",
              "Chepstow, Monmouthshire, Wales",
              "Chester, Cheshire, England",
              "Chesterfield, Derbyshire, England",
              "Chichester, Sussex, England",
              "Chipping Norton, Oxfordshire, England",
              "Chorley, Lancashire, England",
              "Christchurch, Hampshire, England",
              "Cirencester, Gloucestershire, England",
              "Clitheroe, Lancashire, England",
              "Clonmel, Tipperary, Republic of Ireland",
              "Cockermouth, Cumberland, England",
              "Colchester, Essex, England",
              "Coleraine, Londonderry, Northern Ireland",
              "Congleton, Cheshire, England",
              "Cookstown, Tyrone, Northern Ireland",
              "Cork, Cork, Republic of Ireland",
              "Coventry, Warwickshire, England",
              "Crawley, Sussex, England",
              "Crewe, Cheshire, England",
              "Cupar, Fife, Scotland",
              "Darlington, Durham, England",
              "Dartmouth, Devon, England",
              "Denbigh, Denbighshire, Wales",
              "Derby, Derbyshire, England",
              "Devizes, Wiltshire, England",
              "Dewsbury, Yorkshire, England",
              "Dingwall, Ross and Cromarty, Scotland",
              "Diss, Norfolk, England",
              "Doncaster, Yorkshire, England",
              "Dorchester, Dorset, England",
              "Dorking, Surrey, England",
              "Douglas, Isle of Man, Isle of Man",
              "Dover, Kent, England",
              "Downpatrick, Down, Northern Ireland",
              "Driffield, Yorkshire, England",
              "Drogheda, Louth, Republic of Ireland",
              "Dublin, Dublin, Republic of Ireland",
              "Dudley, Worcestershire, England",
              "Dumfries, Dumfriesshire, Scotland",
              "Dundalk, Louth, Republic of Ireland",
              "Dundee, Angus, Scotland",
              "Dunfermline, Fife, Scotland",
              "Dungannon, Tyrone, Northern Ireland",
              "Dunstable, Bedfordshire, England",
              "Durham, Durham, England",
              "East Dereham, Norfolk, England",
              "Eastbourne, Sussex, England",
              "Edinburgh, Midlothian, Scotland",
              "Elgin, Moray, Scotland",
              "Ennis, Clare, Republic of Ireland",
              "Enniscorthy, Wexford, Republic of Ireland",
              "Enniskillen, Fermanagh, Northern Ireland",
              "Epworth, Lincolnshire, England",
              "Evesham, Worcestershire, England",
              "Exeter, Devon, England",
              "Exmouth, Devon, England",
              "Falkirk, Stirlingshire, Scotland",
              "Falmouth, Cornwall, England",
              "Faringdon, Berkshire, England",
              "Faversham, Kent, England",
              "Folkestone, Kent, England",
              "Forfar, Angus, Scotland",
              "Forres, Moray, Scotland",
              "Framlingham, Suffolk, England",
              "Fraserburgh, Aberdeenshire, Scotland",
              "Frome, Somerset, England",
              "Galway, Galway, Republic of Ireland",
              "Glasgow, Lanarkshire, Scotland",
              "Glossop, Derbyshire, England",
              "Gloucester, Gloucestershire, England",
              "Golspie, Sutherland, Scotland",
              "Goole, Yorkshire, England",
              "Grantham, Lincolnshire, England",
              "Gravesend, Kent, England",
              "Grays, Essex, England",
              "Great Yarmouth, Norfolk, England",
              "Greenock, Renfrewshire, Scotland",
              "Grimsby, Lincolnshire, England",
              "Guildford, Surrey, England",
              "Haddington, East Lothian, Scotland",
              "Halesworth, Suffolk, England",
              "Halifax, Yorkshire, England",
              "Hamilton, Lanarkshire, Scotland",
              "Harrogate, Yorkshire, England",
              "Hartland, Devon, England",
              "Hartlepool, Durham, England",
              "Hastings, Sussex, England",
              "Haverfordwest, Pembrokeshire, Wales",
              "Hawick, Roxburghshire, Scotland",
              "Haywards Heath, Sussex, England",
              "Hemel Hempstead, Hertfordshire, England",
              "Henley-on-Thames, Oxfordshire, England",
              "Hereford, Herefordshire, England",
              "Hertford, Hertfordshire, England",
              "Hexham, Northumberland, England",
              "High Wycombe, Buckinghamshire, England",
              "Hitchin, Hertfordshire, England",
              "Horncastle, Lincolnshire, England",
              "Horsham, Sussex, England",
              "Huddersfield, Yorkshire, England",
              "Hull, Yorkshire, England",
              "Huntingdon, Huntingdonshire, England",
              "Hyde, Cheshire, England",
              "Ilfracombe, Devon, England",
              "Ilkeston, Derbyshire, England",
              "Ilkley, Yorkshire, England",
              "Inverness, Inverness-shire, Scotland",
              "Ipswich, Suffolk, England",
              "Jarrow, Durham, England",
              "Jedburgh, Roxburghshire, Scotland",
              "Keighley, Yorkshire, England",
              "Kelso, Roxburghshire, Scotland",
              "Kendal, Westmorland, England",
              "Keswick, Cumberland, England",
              "Kettering, Northamptonshire, England",
              "Kidderminster, Worcestershire, England",
              "Kilkenny, Kilkenny, Republic of Ireland",
              "Kilsyth, Stirlingshire, Scotland",
              "Kinross, Kinross-shire, Scotland",
              "Kirkcaldy, Fife, Scotland",
              "Kirkintilloch, Dunbartonshire, Scotland",
              "Kirkwall, Orkney, Scotland",
              "Knaresborough, Yorkshire, England",
              "Lanark, Lanarkshire, Scotland",
              "Lancaster, Lancashire, England",
              "Larne, Antrim, Northern Ireland",
              "Launceston, Cornwall, England",
              "Leamington, Warwickshire, England",
              "Leeds, Yorkshire, England",
              "Leek, Staffordshire, England",
              "Leicester, Leicestershire, England",
              "Leigh, Lancashire, England",
              "Leighton Buzzard, Bedfordshire, England",
              "Leominster, Herefordshire, England",
              "Lerwick, Shetland, Scotland",
              "Lewes, Sussex, England",
              "Lichfield, Staffordshire, England",
              "Limerick, Limerick, Republic of Ireland",
              "Lincoln, Lincolnshire, England",
              "Linlithgow, West Lothian, Scotland",
              "Lisburn, Antrim, Northern Ireland",
              "Liskeard, Cornwall, England",
              "Littlehampton, Sussex, England",
              "Liverpool, Lancashire, England",
              "Llandudno, Caernarfonshire, Wales",
              "Llanidloes, Montgomeryshire, Wales",
              "London, London, England",
              "Londonderry, Londonderry, Northern Ireland",
              "Longford, Longford, Republic of Ireland",
              "Loughborough, Leicestershire, England",
              "Louth, Lincolnshire, England",
              "Lowestoft, Suffolk, England",
              "Ludlow, Shropshire, England",
              "Lurgan, Armagh, Northern Ireland",
              "Luton, Bedfordshire, England",
              "Macclesfield, Cheshire, England",
              "Maidstone, Kent, England",
              "Malvern, Worcestershire, England",
              "Manchester, Lancashire, England",
              "Mansfield, Nottinghamshire, England",
              "March, Cambridgeshire, England",
              "Market Harborough, Leicestershire, England",
              "Market Rasen, Lincolnshire, England",
              "Maryport, Cumberland, England",
              "Melton Mowbray, Leicestershire, England",
              "Merthyr Tydfil, Glamorgan, Wales",
              "Middlesbrough, Yorkshire, England",
              "Millom, Cumberland, England",
              "Milngavie, Dunbartonshire, Scotland",
              "Minehead, Somerset, England",
              "Mohill, Leitrim, Republic of Ireland",
              "Monaghan, Monaghan, Republic of Ireland",
              "Monmouth, Monmouthshire, Wales",
              "Morecambe, Lancashire, England",
              "Morpeth, Northumberland, England",
              "Motherwell, Lanarkshire, Scotland",
              "Mullingar, Westmeath, Republic of Ireland",
              "Naas, Kildare, Republic of Ireland",
              "Nairn, Nairn, Scotland",
              "Nantwich, Cheshire, England",
              "Navan, Meath, Republic of Ireland",
              "Nelson, Lancashire, England",
              "Nenagh, Tipperary, Republic of Ireland",
              "Newbury, Berkshire, England",
              "Newcastle-upon-Tyne, Northumberland, England",
              "Newport Pagnell, Buckinghamshire, England",
              "Newport, Isle of Wight, England",
              "Newport, Monmouthshire, Wales",
              "Newry, Down, Northern Ireland",
              "Newton Abbot, Devon, England",
              "Newton Stewart, Wigtownshire, Scotland",
              "Newton, Montgomeryshire, Wales",
              "Northampton, Northamptonshire, England",
              "Northwich, Cheshire, England",
              "Norwich, Norfolk, England",
              "Nottingham, Nottinghamshire, England",
              "Nuneaton, Warwickshire, England",
              "Oakham, Rutland, England",
              "Oban, Argyll, Scotland",
              "Offaly, Offaly, Republic of Ireland",
              "Omagh, Tyrone, Northern Ireland",
              "Ormskirk, Lancashire, England",
              "Ossett, Yorkshire, England",
              "Oswestry, Shropshire, England",
              "Otley, Yorkshire, England",
              "Oxford, Oxfordshire, England",
              "Paisley, Renfrewshire, Scotland",
              "Pateley Bridge, Yorkshire, England",
              "Peebles, Peeblesshire, Scotland",
              "Penarth, Glamorgan, Wales",
              "Penrith, Cumberland, England",
              "Penzance, Cornwall, England",
              "Perth, Perthshire, Scotland",
              "Peterborough, Northamptonshire, England",
              "Peterhead, Aberdeenshire, Scotland",
              "Petersfield, Hampshire, England",
              "Plymouth, Devon, England",
              "Pontefract, Yorkshire, England",
              "Pontypool, Monmouthshire, Wales",
              "Pontypridd, Glamorgan, Wales",
              "Port Laoise, Laois, Republic of Ireland",
              "Portadown, Armagh, Northern Ireland",
              "Portsmouth, Hampshire, England",
              "Prescot, Lancashire, England",
              "Preston, Lancashire, England",
              "Ramsgate, Kent, England",
              "Reading, Berkshire, England",
              "Redruth, Cornwall, England",
              "Reigate, Surrey, England",
              "Rhyl, Flintshire, Wales",
              "Ripley, Derbyshire, England",
              "Rochdale, Lancashire, England",
              "Rochester, Kent, England",
              "Roscommon, Roscommon, Republic of Ireland",
              "Ross-on-Wye, Herefordshire, England",
              "Rothesay, Buteshire, Scotland",
              "Royston, Hertfordshire, England",
              "Rugby, Warwickshire, England",
              "Ryde, Isle of Wight, England",
              "Saffron Walden, Essex, England",
              "Saint Helier, Jersey, Jersey",
              "Saint Peter Port, Guernsey, Guernsey",
              "Salisbury, Wiltshire, England",
              "Scarborough, Yorkshire, England",
              "Scunthorpe, Lincolnshire, England",
              "Selkirk, Selkirkshire, Scotland",
              "Sevenoaks, Kent, England",
              "Sheffield, Yorkshire, England",
              "Shepton Mallet, Somerset, England",
              "Sherborne, Dorset, England",
              "Shipley, Yorkshire, England",
              "Shrewsbury, Shropshire, England",
              "Sidmouth, Devon, England",
              "Skegness, Lincolnshire, England",
              "Skibbereen, Cork, Republic of Ireland",
              "Skipton, Yorkshire, England",
              "Sligo, Sligo, Republic of Ireland",
              "South Shields, Durham, England",
              "Southampton, Hampshire, England",
              "Southend-on-Sea, Essex, England",
              "Southport, Lancashire, England",
              "Spalding, Lincolnshire, England",
              "St Albans, Hertfordshire, England",
              "St Andrews, Fife, Scotland",
              "St Neots, Huntingdonshire, England",
              "Stafford, Staffordshire, England",
              "Staines, Middlesex, England",
              "Stamford, Lincolnshire, England",
              "Stirling, Stirlingshire, Scotland",
              "Stockport, Cheshire, England",
              "Stoke-on-Trent, Staffordshire, England",
              "Stonehaven, Kincardineshire, Scotland",
              "Stornoway, Ross and Cromarty, Scotland",
              "Stourbridge, Worcestershire, England",
              "Stranraer, Wigtownshire, Scotland",
              "Stroud, Gloucestershire, England",
              "Sudbury, Suffolk, England",
              "Sunderland, Durham, England",
              "Swansea, Glamorgan, Wales",
              "Swindon, Wiltshire, England",
              "Tadcaster, Yorkshire, England",
              "Tamworth, Staffordshire, England",
              "Taunton, Somerset, England",
              "Tenbury Wells, Worcestershire, England",
              "Tenby, Pembrokeshire, Wales",
              "Tewkesbury, Gloucestershire, England",
              "Thame, Oxfordshire, England",
              "Thetford, Norfolk, England",
              "Tiverton, Devon, England",
              "Todmorden, Yorkshire, England",
              "Torquay, Devon, England",
              "Totnes, Devon, England",
              "Tralee, Kerry, Republic of Ireland",
              "Trowbridge, Wiltshire, England",
              "Truro, Cornwall, England",
              "Tuam, Galway, Republic of Ireland",
              "Tunbridge Wells, Kent, England",
              "Tynemouth, Northumberland, England",
              "Ulverston, Lancashire, England",
              "Usk, Monmouthshire, Wales",
              "Wallingford, Berkshire, England",
              "Walsall, Staffordshire, England",
              "Waltham Abbey, Essex, England",
              "Warminster, Wiltshire, England",
              "Warrington, Lancashire, England",
              "Warwick, Warwickshire, England",
              "Waterford, Waterford, Republic of Ireland",
              "Watford, Hertfordshire, England",
              "Wednesbury, Staffordshire, England",
              "Wellington, Shropshire, England",
              "Wells, Somerset, England",
              "Welshpool, Montgomeryshire, Wales",
              "Weston-super-Mare, Somerset, England",
              "Wetherby, Yorkshire, England",
              "Wexford, Wexford, Republic of Ireland",
              "Weymouth, Dorset, England",
              "Whitby, Yorkshire, England",
              "Whitchurch, Shropshire, England",
              "Whitehaven, Cumberland, England",
              "Whitstable, Kent, England",
              "Wick, Caithness, Scotland",
              "Wicklow, Wicklow, Republic of Ireland",
              "Wigan, Lancashire, England",
              "Wigton, Cumberland, England",
              "Winchester, Hampshire, England",
              "Windermere, Westmorland, England",
              "Windsor, Berkshire, England",
              "Winsford, Cheshire, England",
              "Wisbech, Cambridgeshire, England",
              "Witney, Oxfordshire, England",
              "Wolverhampton, Staffordshire, England",
              "Worcester, Worcestershire, England",
              "Workington, Cumberland, England",
              "Worthing, Sussex, England",
              "Wrexham, Denbighshire, Wales",
              "Yeovil, Somerset, England",
              "York, Yorkshire, England"
            ]
        };
    },
};
</script>