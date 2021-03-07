import { mount } from "@vue/test-utils";
import Login from "@/components/layout/Login.vue";

describe("header.vue Test", () => {
    it("renders message when component is created", () => {
        expect.assertions(2);
        // render the component
        const wrapper = mount(Login, {
            data() {
                return {
                    wrongCredentialsProvided: false,
                    username: "test_username",
                    password: "test_password",
                };
            },
        });
        expect(
            wrapper.findAllComponents({ name: "b-input" }).at(0).props().value
        ).toMatch("test_username");
        expect(
            wrapper.findAllComponents({ name: "b-input" }).at(1).props().value
        ).toMatch("test_password");
    });
});
