<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style lang="scss">
	/* 首先导入uview-plus */
	@import "uview-plus/index.scss";
	
	/* 然后导入我们的主题和全局样式 */
	@import "@/static/theme.scss";
	@import "@/static/global.scss";
</style>
