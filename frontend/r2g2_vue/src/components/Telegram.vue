<!-- Telegram Page -->

<template>
  <div class="navigation">
    <Navigation/>
    <!-- <el-button @click="toggleSidebar">
      <Icon
        :icon="showSidebar ? 'material-symbols:play-arrow-outline' : 'material-symbols:play-arrow-outline'"
        :rotate="showSidebar ? 2 : 0"
      />
    </el-button> -->
  </div>
  <el-container class="layout-container">
    <loading :active="isLoading" :is-full-page="true" :loader="loader" />
    <!-- <el-aside width="300px" v-show="showSidebar">
      <el-scrollbar>
        <div class="m-4">
          <h3>{{$t('Choose the topics of interest within the telegram data')}}</h3>
          <el-select
            v-model="selectedNews"
            multiple
            collapse-tags
            collapse-tags-tooltip
            placeholder="Select"
            size="large"
          >
            <el-option
              v-for="item in newsOptions"
              :key="item.value"
              :value="item.value"
            />
          </el-select>
        </div>
        <el-row>
          <div class="empty-line"></div>
        </el-row>
      </el-scrollbar>
    </el-aside> -->
  
    <!-- 主页面/main -->
    <el-main>
      <el-row class="header">
        <h1>{{$t('Identifying the most relevant topics in Telegram related to the Ukrainian refugee crisis')}}</h1>
      </el-row>
      <!-- 第一行/first row -->
      <el-row>
        <!-- 第一行第一列 选择国家/first column in first row, select country -->
        <el-col :span="3"></el-col>
        <el-col :span="5"><div class="grid-content ep-bg-purple"/>
          <!-- <h3>{{$t('Select a country of interest')}}</h3>
          <el-select v-model="selectedCountry" class="m-2" placeholder="Select" size="large" clearable>
            <el-option
              v-for="(country) in countryOptions"
              :key="$t(country)"
              :value="$t(country)"
            />
          </el-select> -->
          <!-- 数据类别选择框/topics selection box -->
          <h3>{{$t('Choose a topic of interest')}}</h3>
          <el-select
            v-model="selectedNews"
            placeholder="Select"
            size="large"
            clearable
          >
            <el-option
              v-for="item in newsOptions"
              :key="item.value"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="1"></el-col>
        <!-- 第一行第二列 选择州/second column in first row, select state -->
        <el-col :span="5"><div class="grid-content ep-bg-purple-light" />
          <h3>{{$t('Choose a state of interest')}}</h3>
          <el-select v-model="selectedState" class="m-2" placeholder="Select" size="large" clearable>
            <el-option
              v-for="item in stateOptions"
              :key="item.value"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="1"></el-col>
        <!-- 第一行第三列 时间轴/third column in first row, time slider -->
        <el-col :span="8"><div class="grid-content ep-bg-purple" />
          <h3>{{$t('Choose date range of interest')}}</h3>
          <DatePicker v-if="minDate !== null && maxDate !== null" :minDate="minDate" :maxDate="maxDate" @selected-date="handleSelectedDate"/>
        </el-col>
      </el-row>
      <!-- 第二行 空行/second row, empty line -->
      <el-row>
        <div class="empty-line"></div>
      </el-row>
      <!-- 第三行/third row -->
      <el-row>
        <!-- 第三行第一列 地图/first column in third row, map -->
        <el-col :span="8">
          <MapComponent ref="mapcomponent" class="map-component"
            :selectedCountry="selectedCountry"
            :selectedState="selectedState"
            @countryAndStateChanged="handleCountryAndStateChanged"
            @stateSelected="handleStateSelected"
          />
        </el-col>
        <!-- 第三行第二列 折线图和chatbot/second column in third row, line chart and chatbot -->
        <el-col :span="16">
          <el-container class="chart-container">
              <LineChart :height="300" :chartData="chartData" :selectedState="selectedState" />
          </el-container>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
  <el-affix position="bottom" :offset="20">
    <el-container class="chatbot">
      <el-popover
        placement="top-start"
        title="Hello!"
        :width="200"
        trigger="hover"
        content="I'm a chatbot, try to ask me some questions.">
        <template #reference>
          <el-button round @click="toggleChatbot">
            <Icon icon="material-symbols:robot-2-outline" width="56" height="56" :horizontalFlip="true" />
            <Icon icon="humbleicons:chat" width="36" height="36"/>
          </el-button>
        </template>
      </el-popover>
    </el-container>
  </el-affix>
  <el-affix position="bottom" :offset="750">
    <el-container class="chatbot-container">
      <ChatBot v-show="showChatbot" 
        :selectedNews="selectedNews" 
        :selectedState="selectedState" 
        :minDate="dateOptions[0]"
        :maxDate="dateOptions[dateOptions.length-1]"/>
    </el-container>
  </el-affix>
</template>
  
  <script>
  import MapComponent from './MapComponent.vue';
  import LineChart from './LineChart.vue';
  import ChatBot from './ChatBot.vue';
  import Navigation from './Navigation.vue';
  import axios from "../router/request";
  import DatePicker from './DatePicker.vue';
  import {Icon} from '@iconify/vue'
  import {
    ArrowRight as arrowright,
    ArrowLeft as arrowleft
  } from '@element-plus/icons-vue';

  export default {
    components: {
      MapComponent,
      LineChart,
      ChatBot,
      Navigation,
      DatePicker,
      arrowright,
      arrowleft,
      Icon,
    },
    data() {
      return {
        dataTele: [],
        cachedData: {},
        isLoading: false,
        fullPage: false,
        loader: "bars",
        showSidebar: false,       // show side bar
        sidebarIcon: arrowright,
        selectedNews: [], // 
        newsOptions: [],         // store clusters options in data
        selectedCountry: '',     // country property, define the current chosen country in web
        countryOptions: ['Switzerland'], // define country options in select box
        // countryOptions: ['all countries analysed', 'Germany', 'Switzerland'],
        selectedState: '',       // state property, define the current chosen state
        stateOptions: [],        // define state options in select box
        selectedDate: null,      // date property, define the date range in time slider
        selectedDateRange: null, // store new date range when slider move
        minDate: null,           // define min date
        maxDate: null,           // define max date
        dateOptions: [],         // define date options in time slider
        chartData: {
          labels: [],
          datasets: [],
        },                       // define data for line chart
        filteredData: [],        // store filtered data
        drawer: false,
        showChatbot: false,
      };
    },
  
    async created(){
        this.isLoading = true;
      
        await this.fetch();

        // get all cluster in array like {1:xx, 2:yy, ...}
        const clusteredData = await this.$getCluster_tele(this.dataTele);
        this.newsOptions = clusteredData.map((cluster) => ({
          value: cluster !== undefined ? cluster : "undefined",
        }));

        // 默认选中 "all found topics"
        this.selectedNews = this.newsOptions.map(option => option.value);
    
        // get all state
        const stateData = await this.$getState_tele(this.dataTele);
        this.stateOptions = stateData.map((state) => ({
            value: state,
        }));
    
        // get the min,max date as well as date range in type 1645660800000
        const dateData = await this.$getDate_tele(this.dataTele);
        this.dateOptions = dateData;
        this.minDate = this.dateOptions[0];
        this.maxDate = this.dateOptions[this.dateOptions.length - 1];
        this.selectedDate = [this.minDate, this.maxDate];
    
        // Load data and draw chart

        const allClustersData = {};
        for (const targetDate of this.dateOptions) {
            const allClustersCount = await this.$countedCluster(this.dataTele, targetDate);
            allClustersData[targetDate] = allClustersCount;
        };

        // moving average
        // const aftermovingAverage = await this.$movingAverage(allClustersData, 21);

        this.chartData = {
            labels: this.dateOptions,
            datasets: this.newsOptions.map((option) => ({
            tension: 0.3,
            label: option.value,
            data: this.dateOptions.map((date) => allClustersData[date][option.value] || 0),
            borderWidth: 2,
            fill: false,
            pointStyle: false,
            }))
        };
        this.filteredData = await this.filterDataByCountryAndState();
        this.isLoading = false;
  
    },
  
    watch: {
        selectedNews: {
            immediate: true,
            handler: 'updateChartData',
        },
        selectedCountryAndState() {
            this.$emit('countryAndStateChanged', {
            selectedCountry: this.selectedCountry,
            selectedState: this.selectedState
            });
        },
        selectedCountry: 'updateCountryAndState',
        selectedState: 'updateCountryAndState',
      
    },

    methods:{
      async fetch() {
          if (this.cachedData.dataTele) {
              this.dataTele = this.cachedData.dataTele;
          } else {
              try {
                  // const response = await axios.get('https://51.20.75.190:8000/aggregate/TelegramCount');
                  const response = await axios.get('https://db.governmentasaplatform.ch/aggregate/TelegramCount', 
                    {withCredentials: true,
                  });
                  this.dataTele = response.data;
                  this.cachedData.dataTele = this.dataTele;
              } catch(error) {
                  console.log(error)
              }
          }
      },  
      DtoE() {
          if (this.selectedCountry === 'Deutschland') {
          return 'Germany'
          } else if (this.selectedCountry === 'Schweiz') {
          return 'Switzerland'
          } else {
          return this.selectedCountry
          }
      },
      async filterDataByCountryAndState() {
          const countrySelected = this.DtoE(this.selectedCountry);
          return this.dataTele.filter((item) => {
            const countryMatch = !countrySelected || item.country === countrySelected;
            const stateMatch = !this.selectedState || item.state === this.selectedState;
          return countryMatch && stateMatch;
          });
      }, 
      async handleSelectedDate(value) {
        if (value === null) {
          return;
        }
        this.dateOptions = await this.$convertTimetoString_tele(value);
        console.log(this.dateOptions[0])
        this.updateChartData();
      },
      async updateChartData() {
          this.selectedCluster = this.selectedNews;
          const ClustersData = {};
          for (const targetDate of this.dateOptions) {
              const clusterCount = await this.$countedCluster(this.filteredData, targetDate, this.selectedCluster);
              ClustersData[targetDate] = clusterCount;
          }
          // moving average
          // const aftermovingAverage = await this.$movingAverage(ClustersData, 21)

          // console.log(aftermovingAverage)
          this.chartData = {
              tension: 0.3,
              labels: this.dateOptions,
              datasets: this.newsOptions.map((option) => ({
                tension: 0.3,
                label: option.value,
                data: this.dateOptions.map((date) => ClustersData[date][option.value] || 0),
                borderWidth: 2,
                fill: false,
                pointStyle: false,
              }))
          };
      },
  
      async updateCountryAndState() {
          if (this.selectedCountry === ('all countries analysed')) {
            this.filteredData = this.dataTele
          } else if (this.selectedCountry === ('alle analysierten Länder')) {
            this.filteredData = this.dataTele
          } else {
            this.filteredData = await this.filterDataByCountryAndState();
          }
          this.updateChartData();
      },
      // handleCountryAndStateChanged({ selectedCountry, selectedState }) {
      //     this.selectedCountry = selectedCountry;
      //     this.selectedState = selectedState;
      // },
      handleStateSelected(selectedState) {
          this.selectedState = selectedState;
      },
      // toggleSidebar() {
      //   this.showSidebar = !this.showSidebar;
      //   this.sidebarIcon = this.showSidebar ? arrowleft : arrowright;
      // },
      toggleChatbot() {
        this.showChatbot = !this.showChatbot;
      },
      // transfer cluster and state to chatbot
    },
  };
  </script>
  
  
  <style scoped> 
  .navigation {
    position: fixed;
    width: 100%;
    z-index: 100;
    top: 0;
    left: 0;
  }
  .layout-container {
    padding-top: 50px;
    display: flex;
    flex-grow: 1;
    overflow-x: hidden;
    background-color: transparent;
    height: 100%;
  }
  .layout-container h3 {
    /* font-family: 'Cantora One', sans-serif; */
    margin-bottom: 30px;
    font-size: 15px;
  }
  .layout-container .m-4 {
    margin-left: 30px;
    margin-top: 30px;
  }
  .header {
    height: 100px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: transparent;
  }
  .layout-container h1 {
    margin: 10px;
    font-size: 30px;
    text-align: center;
    font-size: 28px;
  }
  .layout-container .el-aside {
    color: var(--el-text-color-primary);
    background: var(--el-color-primary-light-8);
  }
  .layout-container .el-main {
    padding: 20px;
    flex-grow: 1;
    overflow-y: hidden;
  }
  .grid-content {
    border-radius: 10px;
    min-height: 10px;
  }
  .empty-line{
    height: 50px;
  }
  /* New styles for the map component */
  .map-component {
    width: 100%;
    height: 100%;
  }
  .chart-container {
    width: 100%;
    height: 100%;
    position: relative;
    flex-grow: 1;
  }
  .chatbot {
    justify-content: center;
    /* align-items: center; */
  }
  .chatbot-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 25%;
    z-index: 999;
  }
  </style>
  
  