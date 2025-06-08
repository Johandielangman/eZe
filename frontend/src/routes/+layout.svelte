<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<svelte:head>
    <title>eZe Finance</title>
</svelte:head>


<div class="min-h-screen flex flex-col">
	<div class="p-7">
		{@render children()}
	</div>
</div>
