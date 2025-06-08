<script lang="ts">
	let { data } = $props();
</script>

<div class="text-center p-6">
	<h1 class="text-2xl font-bold mb-4">Signup Successful 🎉</h1>
	<p class="text-gray-700 mb-2">Your account has been created.</p>
	<p class="text-sm text-gray-600">
		Your user ID: <code class="bg-gray-100 px-2 py-1 rounded">{data.id}</code>
	</p>

	<a href="/auth/login" class="inline-block mt-6 text-blue-600 hover:underline">
		Go to login
	</a>
</div>
