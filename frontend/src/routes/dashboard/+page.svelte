<script>
	import Footer from '$lib/Footer.svelte';
	import Header from '$lib/Header.svelte';
	export let data;
</script>

<svelte:head>
	<title>Kinde Auth | SvelteKit Starter Kit</title>
</svelte:head>

<Header isAuthenticated={data.isAuthentication} user={data.userProfile} />

<main>
	<div class="container">
		<div class="card hero">
			<p class="text-display-1 hero-title">
				{data.pingResponse} from backend!
			</p>
		</div>
	</div>
</main>
<Footer />
