<template>
  <div class="">
    <div class="my-4 flex sm:flex-row flex-col">
        <div class="flex flex-row mb-1 sm:mb-0">
            <div class="relative">
                <select v-model="filterStatus"
                class="appearance-none h-full rounded-l border block  w-full bg-white border-gray-400 text-gray-700 py-2 px-4 pr-8 leading-tight focus:outline-none focus:bg-white focus:border-gray-500">
                   <option value="">All</option>
                    <option value="due">Due</option>
                    <option value="received">Received</option>
                    <option value="to_be_verified">To be Verified</option>
                    <option value="verified">Verified</option>
                    <option value="published">Published</option>
                    <option value="invalidated">Invalidated</option>
                    <option value="cancelled">Cancelled</option>
                    <option value="rejected">Rejected</option>
                </select>
                <div
                    class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                        <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                    </svg>
                </div>
            </div>
        </div>
        <div class="block relative">
            <span class="h-full absolute inset-y-0 left-0 flex items-center pl-2">
                <svg viewBox="0 0 24 24" class="h-4 w-4 fill-current text-gray-500">
                    <path
                        d="M10 4a6 6 0 100 12 6 6 0 000-12zm-8 6a8 8 0 1114.32 4.906l5.387 5.387a1 1 0 01-1.414 1.414l-5.387-5.387A8 8 0 012 10z">
                    </path>
                </svg>
            </span>
            <input placeholder="Search ..."
                v-model="filterText"
                class="appearance-none rounded-r rounded-l sm:rounded-l-none border border-gray-400 border-b block pl-8 pr-6 py-2 w-full bg-white text-sm placeholder-gray-400 text-gray-700 focus:bg-white focus:placeholder-gray-600 focus:text-gray-700 focus:outline-none" />
        </div><button @click.prevent="filterSamples()"
      class="px-2 py-1 ml-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Filter ...</button>
      
    </div>

    <hr>
    <router-link to="/patients/search" class="px-2 py-1 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Add Laboratory Request</router-link>
    <hr>

    <!-- Sampe Table View -->
    <div class="overflow-x-auto mt-4">
        <div class="align-middle inline-block min-w-full shadow overflow-hidden bg-white shadow-dashboard px-2 pt-1 rounded-bl-lg rounded-br-lg">
        <table class="min-w-full">
            <thead>
            <tr>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left leading-4 text-black-500 tracking-wider">
                    <input type="checkbox" @change="toggleCheckAll()" v-model="allChecked">
                </th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left leading-4 text-black-500 tracking-wider"></th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left leading-4 text-black-500 tracking-wider">Sampe ID</th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left text-sm leading-4 text-black-500 tracking-wider">Test(s)</th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left text-sm leading-4 text-black-500 tracking-wider">Patient</th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left text-sm leading-4 text-black-500 tracking-wider">Client Patient ID</th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left text-sm leading-4 text-black-500 tracking-wider">Client</th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left text-sm leading-4 text-black-500 tracking-wider">Created</th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left text-sm leading-4 text-black-500 tracking-wider">Creator</th>
                <th class="px-1 py-1 border-b-2 border-gray-300 text-left text-sm leading-4 text-black-500 tracking-wider">Status</th>
                <th class="px-1 py-1 border-b-2 border-gray-300"></th>
            </tr>
            </thead>
            <tbody class="bg-white" v-if="samples?.length > 0">
              <tr
                  v-for="sample in samples" :key="sample.uid"
              >
                  <td>
                      <input type="checkbox" v-model="sample.checked" @change="checkCheck(sample)">
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                      <span v-if="sample.priority! > 1"
                      :class="[
                          'font-small',
                          { 'text-red-700': sample.priority! > 1 },
                      ]">
                          <i class="fa fa-star"></i>
                      </span>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <div class="flex items-center">
                      <div class="text-sm leading-5 text-gray-800">
                        <router-link :to="{ name: 'sample-detail', params: { patientUid: sample?.analysisRequest?.patient?.uid, sampleUid:sample?.uid  }}">{{ sample.sampleId }}</router-link>
                      </div>
                  </div>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <div class="text-sm leading-5 text-blue-900">{{ profileAnalysesText(sample.profiles!, sample.analyses!) }}</div>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <div class="text-sm leading-5 text-blue-900">{{ sample?.analysisRequest?.patient?.firstName }} {{ sample?.analysisRequest?.patient?.lastName }}</div>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <div class="text-sm leading-5 text-blue-900">{{ sample?.analysisRequest?.patient?.clientPatientId }}</div>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <div class="text-sm leading-5 text-blue-900">{{ sample?.analysisRequest?.client?.name }}</div>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <div class="text-sm leading-5 text-blue-900">10/10/2020</div>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <div class="text-sm leading-5 text-blue-900">Amos T ...</div>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap border-b border-gray-500">
                  <button type="button" class="bg-blue-400 text-white p-1 rounded leading-none">{{ sample.status }}</button>
                  </td>
                  <td class="px-1 py-1 whitespace-no-wrap text-right border-b border-gray-500 text-sm leading-5">
                      <!-- <button class="px-2 py-1 mr-2 border-orange-500 border text-orange-500 rounded transition duration-300 hover:bg-orange-700 hover:text-white focus:outline-none">View</button> -->
                      <button class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">View</button>
                  </td>
              </tr>
            </tbody>
        </table>
        </div>
    </div>


  <section class="flex justify-between items-center">
    <div>
         <button 
         v-show="can_cancel" 
         @click.prevent="cancelSamples_()" 
         class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Cancel</button>
         <button 
         v-show="can_reinstate" 
         @click.prevent="reInstateSamples_()" 
         class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">ReInstate</button>
         <button 
         v-show="can_receive" 
         @click.prevent="receiveSamples_()" 
         class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Reveive</button>
         <button v-show="can_reject" 
         @click.prevent="prepareRejections()" 
          class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Reject</button>
         <button v-show="can_copy_to" class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Copy to New</button>
         <button 
         v-show="can_download" 
         @click.prevent="downloadReports_()" 
         class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Download</button>
         <button 
         v-show="can_print" 
         @click.prevent="printReports_()" 
         class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none">Print</button>
    </div>
    <div class="my-4 flex sm:flex-row flex-col">
      <button 
      @click.prevent="showMoreSamples()"
      v-show="pageInfo?.hasNextPage"
      class="px-2 py-1 mr-2 border-blue-500 border text-blue-500 rounded transition duration-300 hover:bg-blue-700 hover:text-white focus:outline-none"
      >Show More</button>
      <div class="flex flex-row mb-1 sm:mb-0">
          <div class="relative">
              <select class="appearance-none h-full rounded-l border block  w-full bg-white border-gray-400 text-gray-700 py-2 px-4 pr-8 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
               v-model="sampleBatch" :disabled="!pageInfo?.hasNextPage">
                  <option value="25">25</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                  <option value="250">250</option>
                  <option value="500">500</option>
                  <option value="1000">1000</option>
                  <option value="5000">5000</option>
                  <option value="10000">10000</option>
              </select>
              <div
                  class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                  <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                      <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                  </svg>
              </div>
          </div>
      </div>
      <div class="block relative">
          <input :placeholder="sampleCount"
              class="appearance-none rounded-r rounded-l sm:rounded-l-none border border-gray-400 border-b block pl-8 pr-6 py-2 w-full bg-white text-sm placeholder-gray-400 text-gray-700 focus:bg-white focus:placeholder-gray-600 focus:text-gray-700 focus:outline-none" disabled/>
      </div>
    </div>
  </section>
  </div>
</template>

<script lang="ts">
import modal from '../../components/SimpleModal.vue';
import { defineComponent, toRefs, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ActionTypes as SampleActionTypes } from '../../store/modules/sample';
import { ActionTypes } from '../../store/modules/analysis';
import { IAnalysisProfile, IAnalysisService, ISample } from '../../models/analysis';
import { ifZeroEmpty } from '../../utils'
import useReportComposable from '../../modules/reports'; 
import useSampleComposable from '../../modules/samples';

export default defineComponent({
  name: "Samples",
  components: {
      modal,
  },
  setup() {    
    const store = useStore();
    let route = useRoute();
    let router = useRouter();

    const state = reactive({
      filterText: "",
      filterStatus: "",
      sampleBatch: 50,
      samples: computed<ISample[]>(() => store.getters.getSamples ),
      pageInfo: computed(() => store.getters.getSamplePageInfo),
      can_cancel:  false,
      can_receive:  false,
      can_reinstate:  false,
      can_reject:  false,
      can_copy_to:  false,
      can_download: false,
      can_print:  false,
      allChecked: false,
    })

    store.dispatch(SampleActionTypes.RESET_SAMPLES);
    store.dispatch(SampleActionTypes.FETCH_SAMPLE_TYPES);

    let analysesParams = reactive({ 
      first: undefined, 
      after: "",
      text: "", 
      sortBy: ["name"]
    });
    store.dispatch(ActionTypes.FETCH_ANALYSES_SERVICES, analysesParams);
    store.dispatch(ActionTypes.FETCH_ANALYSES_PROFILES);


    let sampleParams = reactive({ 
      first: state.sampleBatch, 
      after: "",
      status: "", 
      text: "", 
      sortBy: ["uid"],
      clientUid: +ifZeroEmpty(route?.query?.clientUid),
      filterAction: false
    });

    store.dispatch(SampleActionTypes.FETCH_SAMPLES, sampleParams);

    function profileAnalysesText(profiles: IAnalysisProfile[], analyses: IAnalysisService[]): string {
        let names: string[]= [];
        profiles.forEach(p => names.push(p.name!));
        analyses.forEach(a => names.push(a.name!));
        return names.join(', ');
    }

    function showMoreSamples(): void {
      sampleParams.first = state.sampleBatch;
      sampleParams.after = state.pageInfo?.value?.endCursor;
      sampleParams.text = state.filterText;
      sampleParams.status = state.filterStatus;
      sampleParams.filterAction = false;
      store.dispatch(SampleActionTypes.FETCH_SAMPLES, sampleParams);
    }

    function filterSamples(): void {
      state.sampleBatch = 50;
      sampleParams.first = 50;
      sampleParams.after = "";
      sampleParams.text = state.filterText;
      sampleParams.status = state.filterStatus;
      sampleParams.filterAction = true;
      store.dispatch(SampleActionTypes.FETCH_SAMPLES, sampleParams);
    }

    // user actions perms
    
    function check(sample: ISample): void {
      sample.checked = true;
      checkUserActionPermissios()
    }

    function unCheck(sample: ISample): void {
      sample.checked = false;
      checkUserActionPermissios()
    }

    function toggleCheckAll(): void {
      state.samples?.forEach((sample: ISample) => state.allChecked ? check(sample) : unCheck(sample));
      checkUserActionPermissios()
    }
    
    function areAllChecked(): Boolean {
      return state.samples?.every((sample: ISample) => sample.checked === true);
    }

    function checkCheck(sample: ISample): void {
     if(areAllChecked()) {
        state.allChecked = true;
     } else {
        state.allChecked = false;
     }
      checkUserActionPermissios()
    }

    function getSamplesChecked(): ISample[] {
      let box:ISample[] = [];
      state.samples?.forEach((sample: ISample) => {
        if (sample.checked) box.push(sample);
      });
      return box;
    }

    function checkUserActionPermissios(): void {
      // reset
      state.can_cancel = false;
      state.can_receive = false;
      state.can_reinstate = false;
      state.can_download = false;
      state.can_print = false;
      state.can_reject = false;

      const checked: ISample[] = getSamplesChecked();
      if(checked.length === 0) return;

      // can_receive
      if(checked.every((sample: ISample) => sample.status === 'due')){
        state.can_receive = true;
      }

      // can_cancel
      if(checked.every((sample: ISample) => ["received", "due"].includes(sample.status!))){
        state.can_cancel = true;
        state.can_reject = true;
      }

      // can_reinstate
      if(checked.every((sample: ISample) => sample.status === 'cancelled')){
        state.can_reinstate = true;
      }

      // can_download
      if(checked.every((sample: ISample) => ["verified", "published"].includes(sample.status!))){
        state.can_download = true;
      }

      // can_print
      if(checked.every((sample: ISample) => sample.status === 'verified')){
        state.can_print = true;
      }
    }

    function getSampleUids(): number[] {
      const items: ISample[] = getSamplesChecked();
      let ready: number[] = [];
      items?.forEach(item => ready.push(item.uid!))
      return ready;
    }

    //
    const { cancelSamples, reInstateSamples, receiveSamples, publishSamples }  = useSampleComposable();
    const { downloadReports } =  useReportComposable();
    //
    return {
      ...toRefs(state),
      sampleCount: computed(() => store.getters.getSamples?.length + " of " + store.getters.getSampleCount + " samples"),
      showMoreSamples,
      filterSamples,
      profileAnalysesText,
      toggleCheckAll,
      checkCheck,
      cancelSamples_: async () => cancelSamples(getSampleUids()),
      reInstateSamples_: async () => reInstateSamples(getSampleUids()),
      receiveSamples_: async () => receiveSamples(getSampleUids()),
      downloadReports_: async () => await downloadReports(getSampleUids()),
      printReports_: async () => await publishSamples(getSampleUids()),
      prepareRejections: async () => {
        const selection = getSamplesChecked();
        router.push({ name: "reject-samples", params: { samples: JSON.stringify(selection) }})
      },
    };
  },
});
</script>
