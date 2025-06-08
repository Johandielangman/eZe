import { fail, redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ request }: import('@sveltejs/kit').RequestEvent) => {
		const formData = await request.formData();
		const name = formData.get('name');
		const surname = formData.get('surname');
		const email = formData.get('email');
		const password = formData.get('password');

		let data;

		try {
			const res = await fetch('http://127.0.0.1:8081/v1/users', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ name, surname, email, password })
			});

            if (!res.ok) {
                const error = await res.json();
                if (res.status === 422 && error.detail) {
                    return fail(422, {
                        error: error.detail.map((e: any) => e.msg).join(', '),
                        values: { name, surname, email }
                    });
                }
                return fail(res.status, {
                    error: error.message || 'Signup failed',
                    values: { name, surname, email }
                });
            }

			data = await res.json();
		} catch (err) {
			console.error('Signup error:', err);
			return fail(500, {
				error: 'Server error. Please try again later.',
				values: { name, surname, email }
			});
		}

		throw redirect(303, `/auth/signup-success?id=${data.id}`);
	}
};
