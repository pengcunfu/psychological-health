<template>
  <view class="container">
    <view class="header">
      <text class="title">{{ title }}</text>
      <text class="date">更新日期：2025年8月1日</text>
    </view>

    <view class="content">
      <template v-if="type === 'user'">
        <view class="section">
          <view class="section-title">1. 总则</view>
          <view class="section-content">
            <view class="paragraph">1.1 本协议是用户（"您"）与心理健康平台（"我们"）之间关于您使用我们平台服务的法律协议。</view>
            <view class="paragraph">1.2 在您使用我们的服务之前，请您务必审慎阅读、充分理解本协议各条款内容。</view>
            <view class="paragraph">1.3 如您对本协议有任何疑问，可联系我们的客服咨询。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">2. 账号注册与使用</view>
          <view class="section-content">
            <view class="paragraph">2.1 您在注册账号时应提供真实、准确、完整的个人资料，并及时更新。</view>
            <view class="paragraph">2.2 您应妥善保管账号及密码信息，因您保管不善造成的损失由您自行承担。</view>
            <view class="paragraph">2.3 您的账号仅限您本人使用，不得出借、转让或授权他人使用。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">3. 服务内容与规则</view>
          <view class="section-content">
            <view class="paragraph">3.1 我们提供的服务包括但不限于：心理咨询预约、心理课程学习、心理测评等。</view>
            <view class="paragraph">3.2 您应遵守中华人民共和国相关法律法规及平台规则使用我们的服务。</view>
            <view class="paragraph">3.3 您不得利用我们的服务从事违法活动或损害他人合法权益的行为。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">4. 隐私保护</view>
          <view class="section-content">
            <view class="paragraph">4.1 我们高度重视您的隐私保护，将按照《隐私政策》收集、使用、存储和保护您的个人信息。</view>
            <view class="paragraph">4.2 未经您的同意，我们不会向第三方披露您的个人信息，法律法规另有规定的除外。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">5. 付费服务</view>
          <view class="section-content">
            <view class="paragraph">5.1 部分服务可能需要您付费使用，具体收费标准以页面展示为准。</view>
            <view class="paragraph">5.2 您应按照平台规定的支付方式和时间支付相应费用。</view>
            <view class="paragraph">5.3 退款规则详见各服务的具体说明。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">6. 免责声明</view>
          <view class="section-content">
            <view class="paragraph">6.1 平台提供的心理健康服务不能替代专业医疗机构的诊断和治疗。</view>
            <view class="paragraph">6.2 对于因不可抗力、系统故障、第三方原因等导致的服务中断或信息丢失，平台不承担责任。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">7. 协议修改</view>
          <view class="section-content">
            <view class="paragraph">7.1 我们保留随时修改本协议的权利，修改后的协议将通过平台公告或其他方式通知您。</view>
            <view class="paragraph">7.2 如您继续使用我们的服务，视为您接受修改后的协议。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">8. 法律适用与争议解决</view>
          <view class="section-content">
            <view class="paragraph">8.1 本协议的订立、执行和解释及争议的解决均适用中华人民共和国法律。</view>
            <view class="paragraph">8.2 如发生争议，双方应友好协商解决；协商不成的，任何一方均可向平台所在地有管辖权的人民法院提起诉讼。</view>
          </view>
        </view>
      </template>

      <template v-else-if="type === 'counselor'">
        <view class="section">
          <view class="section-title">1. 总则</view>
          <view class="section-content">
            <view class="paragraph">1.1 本协议是咨询师（"您"）与心理健康平台（"我们"）之间关于您在平台提供心理咨询服务的法律协议。</view>
            <view class="paragraph">1.2 在您申请成为平台咨询师之前，请您务必审慎阅读、充分理解本协议各条款内容。</view>
            <view class="paragraph">1.3 如您对本协议有任何疑问，可联系我们的客服咨询。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">2. 入驻条件与流程</view>
          <view class="section-content">
            <view class="paragraph">2.1 您应具备相关专业资质和执业经验，提供真实、有效的资质证明材料。</view>
            <view class="paragraph">2.2 您需通过平台的资质审核、专业面试等环节，方可正式入驻。</view>
            <view class="paragraph">2.3 您应参加平台组织的培训，了解平台规则和操作流程。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">3. 服务规范</view>
          <view class="section-content">
            <view class="paragraph">3.1 您应遵循专业伦理规范提供心理咨询服务，确保服务质量。</view>
            <view class="paragraph">3.2 您应按照预约时间准时提供服务，不得无故迟到或缺席。</view>
            <view class="paragraph">3.3 您应对来访者的信息严格保密，未经来访者同意不得向第三方透露。</view>
            <view class="paragraph">3.4 您不得利用平台从事违法活动或损害他人合法权益的行为。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">4. 收费与结算</view>
          <view class="section-content">
            <view class="paragraph">4.1 您可在平台规定范围内自主设定咨询费用。</view>
            <view class="paragraph">4.2 平台将按约定比例收取服务费，具体比例以双方签订的合作协议为准。</view>
            <view class="paragraph">4.3 平台将按照约定周期与您进行结算，将款项转入您指定的账户。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">5. 评价机制</view>
          <view class="section-content">
            <view class="paragraph">5.1 来访者可对您的服务进行评价，评价结果将影响您在平台的展示排序和声誉。</view>
            <view class="paragraph">5.2 平台定期对咨询师进行服务质量评估，评估结果可能影响您继续在平台提供服务的资格。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">6. 知识产权</view>
          <view class="section-content">
            <view class="paragraph">6.1 您在平台上发布的原创内容，其知识产权归您所有。</view>
            <view class="paragraph">6.2 您授权平台在服务范围内使用您的姓名、头像、简介等信息。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">7. 协议终止</view>
          <view class="section-content">
            <view class="paragraph">7.1 您可提前30天书面通知平台终止本协议。</view>
            <view class="paragraph">7.2 如您违反本协议或平台规则，平台有权暂停或终止与您的合作。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">8. 法律适用与争议解决</view>
          <view class="section-content">
            <view class="paragraph">8.1 本协议的订立、执行和解释及争议的解决均适用中华人民共和国法律。</view>
            <view class="paragraph">8.2 如发生争议，双方应友好协商解决；协商不成的，任何一方均可向平台所在地有管辖权的人民法院提起诉讼。</view>
          </view>
        </view>
      </template>

      <template v-else>
        <view class="section">
          <view class="section-title">1. 总则</view>
          <view class="section-content">
            <view class="paragraph">1.1 本协议是用户（"您"）与心理健康平台（"我们"）之间关于您使用我们平台服务的法律协议。</view>
            <view class="paragraph">1.2 在您使用我们的服务之前，请您务必审慎阅读、充分理解本协议各条款内容。</view>
            <view class="paragraph">1.3 如您对本协议有任何疑问，可联系我们的客服咨询。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">2. 账号注册与使用</view>
          <view class="section-content">
            <view class="paragraph">2.1 您在注册账号时应提供真实、准确、完整的个人资料，并及时更新。</view>
            <view class="paragraph">2.2 您应妥善保管账号及密码信息，因您保管不善造成的损失由您自行承担。</view>
            <view class="paragraph">2.3 您的账号仅限您本人使用，不得出借、转让或授权他人使用。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">3. 服务内容与规则</view>
          <view class="section-content">
            <view class="paragraph">3.1 我们提供的服务包括但不限于：心理咨询预约、心理课程学习、心理测评等。</view>
            <view class="paragraph">3.2 您应遵守中华人民共和国相关法律法规及平台规则使用我们的服务。</view>
            <view class="paragraph">3.3 您不得利用我们的服务从事违法活动或损害他人合法权益的行为。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">4. 隐私保护</view>
          <view class="section-content">
            <view class="paragraph">4.1 我们高度重视您的隐私保护，将按照《隐私政策》收集、使用、存储和保护您的个人信息。</view>
            <view class="paragraph">4.2 未经您的同意，我们不会向第三方披露您的个人信息，法律法规另有规定的除外。</view>
          </view>
        </view>

        <view class="section">
          <view class="section-title">5. 其他条款</view>
          <view class="section-content">
            <view class="paragraph">5.1 本协议的最终解释权归心理健康平台所有。</view>
            <view class="paragraph">5.2 如您继续使用我们的服务，视为您接受本协议的全部条款。</view>
          </view>
        </view>
      </template>
    </view>
  </view>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

export default {
  setup() {
    const type = ref('user')
    
    const title = computed(() => {
      switch (type.value) {
        case 'counselor':
          return '咨询师服务协议'
        case 'privacy':
          return '隐私政策'
        default:
          return '用户服务协议'
      }
    })
    
    onLoad((options) => {
      if (options.type) {
        type.value = options.type
      }
    })
    
    return {
      type,
      title
    }
  }
}
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #fff;
  padding-bottom: 50rpx;
}

.header {
  padding: 40rpx 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
  text-align: center;
}

.date {
  font-size: 24rpx;
  color: #999;
  display: block;
  text-align: center;
}

.content {
  padding: 30rpx;
}

.section {
  margin-bottom: 40rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.section-content {
  padding-left: 20rpx;
}

.paragraph {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
  margin-bottom: 20rpx;
  text-align: justify;
}
</style> 