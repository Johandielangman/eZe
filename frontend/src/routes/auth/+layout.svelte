<script lang="ts">
	let { children } = $props();
</script>

<svelte:head>
    <title>eZe Finance</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center p-4">
	{@render children()}
</div>
