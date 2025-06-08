<script lang="ts">
	let { form } = $props();
</script>

<div class="w-full max-w-sm bg-white rounded-2xl shadow-md p-6">
	<h1 class="text-2xl font-bold mb-6 text-center">Sign Up</h1>

	{#if form?.error}
		<p class="text-red-600 text-sm mb-4 text-center">{form.error}</p>
	{/if}

	<form method="POST" class="space-y-4">
		<div>
			<label for="name" class="block text-sm font-medium text-gray-700">Name</label>
			<input
				id="name"
				name="name"
				type="text"
				required
				value={form?.values?.name || ''}
				class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>
		</div>

		<div>
			<label for="surname" class="block text-sm font-medium text-gray-700">Surname</label>
			<input
				id="surname"
				name="surname"
				type="text"
				required
				value={form?.values?.surname || ''}
				class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>
		</div>

		<div>
			<label for="email" class="block text-sm font-medium text-gray-700">Email</label>
			<input
				id="email"
				name="email"
				type="email"
				required
				value={form?.values?.email || ''}
				class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>
		</div>

		<div>
			<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
			<input
				id="password"
				name="password"
				type="password"
				required
				class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>
		</div>

		<button
			type="submit"
			class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
		>
			Create Account
		</button>
	</form>

	<p class="text-sm text-center text-gray-600 mt-4">
		Already have an account?
		<a href="/login" class="text-blue-600 hover:underline">Log in</a>
	</p>
</div>
