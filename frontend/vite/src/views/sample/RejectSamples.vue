<template>

  <h4>Sample Rejection</h4>
  <div v-for="(sample, index) in rejections" :key="index">
    <hr class="my-4">
    <h2 class="text-gray-800 font-bold">{{ sample?.sampleId }} &rarr; {{ sample?.status }}</h2>
    <div class="grid grid-cols-12 gap-1 mt-2">
      <div class="col-span-6 grid grid-cols-2 gap-1">
        <div class="col-span-1">
          <div class="flex w-full">
            <span class="text-gray-700 font-semibold w-4/12">Sample Type</span>
            <span>{{ sample?.sampleType?.name }}</span>
          </div>
          <div class="flex w-full">
            <span class="text-gray-700 font-semibold w-4/12">Client Sample ID</span>
            <span>{{ sample?.analysisRequest?.clientRequestId }}</span>
          </div>
          <div class="flex w-full">
            <span class="text-gray-700 font-semibold w-4/12">Anayses</span>
            <span>{{ profileAnalysesText(sample?.profiles, sample?.analyses) }}</span>
          </div>
        </div>
        <div class="col-span-1">
          <div class="flex w-full">
            <span class="text-gray-700 font-semibold w-4/12">Patient</span>
            <span>{{ sample?.analysisRequest?.patient?.firstName }} {{ sample?.analysisRequest?.patient?.lastName }}</span>
          </div>
          <div class="flex w-full">
            <span class="text-gray-700 font-semibold w-4/12">Client Patient ID</span>
            <span>{{ sample?.analysisRequest?.patient?.clientPatientId }}</span>
          </div>
        </div>
      </div>
      <div class="col-span-5">
        <div class="grid grid-cols-2 gap-2">
          <div class="col-span-1">
            <label class="flex flex-col whitespace-nowrap w-full">
              <span class="text-gray-800 font-bold">Rejection Reasons</span>
              <hr>
              <select 
                name="reasons"
                rows="3"
                class="form-input mt-1" multiple v-model="sample.reasons">
                  <option value=""></option>
                  <option 
                  v-for="rejection in rejectionReasons"
                  :key="rejection.uid"
                  :value="rejection.uid">{{ rejection.reason }}</option>
              </select>
            </label>
          </div>
          <div class="col-span-1">
            <label class="flex flex-col whitespace-nowrap w-full">
              <span class="text-gray-700 font-bold">Other</span>
              <hr>
              <input type="text" class="form-input mt-1 block w-full" v-model="sample.other" />
            </label>
          </div>
        </div>
      </div>
      <div class="col-span-1 pt-4 pl-4">
        <button 
          v-show="index === 0" 
          class="ml-4 mt-4"
          @click="cascadeCopy(sample)">
          <font-awesome-icon icon="level-down-alt" />
        </button>
      </div>
    </div>
  </div>

  <button
    v-if="rejections?.length > 0"
    @click.prevent="rejectSamples_()"
    class="px-2 py-1 mr-2 border-red-500 border text-red-500 rounded transition duration-300 hover:bg-red-700 hover:text-white focus:outline-none">Reject Samples</button>


</template>

<script lang="ts">
import { defineComponent, toRefs, computed, onMounted, reactive} from 'vue';
import {useStore } from 'vuex';
import { IAnalysisProfile, IAnalysisService } from '../../models/analysis';
import  useSampleComposable  from '../../modules/samples'
import { ActionTypes } from '../../store/modules/analysis';

  export default defineComponent({
    name: 'sample-rejection',
    props: {
      samples: {
        type: String,
        required: true,
      }
    },
    setup(props) {
      const store = useStore();
      const { rejectSamples } = useSampleComposable(); 

      const { samples } = toRefs(props);

      const state = reactive({
        rejections: [] as any[],
      });

      const ss = JSON.parse(samples.value)
      let coll: any[] = [];
      for(let ob of ss){
        ob["reasons"] = []
        ob["other"] = undefined
        coll.push(ob);
      }
      state.rejections = coll;

      onMounted(() => store.dispatch(ActionTypes.FETCH_REJECTION_REASONS))

      return {
        ...toRefs(state),
        profileAnalysesText: ((profiles: IAnalysisProfile[], analyses: IAnalysisService[]) => {
          let names: string[] = [];
          profiles?.forEach(p => names.push(p.name!));
          analyses?.forEach(a => names.push(a.name!));
          return names.join(', ');
        }),
        cascadeCopy: (sample: any) => {
          state.rejections?.forEach(item => {
            item.reasons = sample.reasons;
            item.other = sample.other;
          })
        }, 
        rejectionReasons: computed(() =>store.getters.getRejectionReasons),
        rejectSamples_: async () => {
          const toReject:any[] = [];
          state.rejections?.forEach(item => {
            toReject.push({ uid: item?.uid, reasons: item?.reasons, other: item?.other })
          })
          await rejectSamples(toReject);
        }
      }
    },
  });

</script>
