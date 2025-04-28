<script setup lang="ts">
import type { components } from '#open-fetch-schemas/backend';
import type { TableColumn, TableRow } from '@nuxt/ui';


const tabs = [{
    slot: 'roles',
    label: 'Ролі'
},{
    slot: 'permissions',
    label: 'Дозволи'
}]

const roleColumns: TableColumn<components["schemas"]["RoleRead"]>[] = [{
    header: '#',
    accessorKey: 'role_id'
}, {
    header: 'Назва',
    accessorKey: 'name'
}, {
    header: 'Дозволи',
    accessorKey: 'permissions',
    cell: ({row}) => {
        const permissions: Array<components["schemas"]["PermissionRead"]> = row.getValue("permissions")
        const badges = permissions.map((permission) => {
            return h(resolveComponent('UBadge'), {label: `${permission.action}:${permission.resource}`, variant:'subtle'})
        })
        return h(resolveComponent("UPopover"), null, {
            default: () => h(resolveComponent("UButton"), {label: permissions.length, class: 'rounded-full'}),
            content: () => h('div', {class:'p-2 grid grid-cols-4 gap-4'}, badges)
        })
    }  
}, {
    header: '',
    accessorKey: 'actions'
}]

const permissionColumns: TableColumn<components["schemas"]["PermissionRead"]>[] = [{
    header: '#',
    accessorKey: 'permission_id',
},{
    header: 'Ресурс',
    accessorKey: 'resource'
}, {
    header: 'Дія',
    accessorKey: 'action'
}, {
    header: '',
    accessorKey: 'actions'
}]

definePageMeta({
    resource: 'roles'
})

</script>

<template>
<div class="w-full h-full">
    <UTabs :items="tabs" variant="link">
        <template #roles>
            <ItemTable title="Ролі" url="/api/v1/roles/" :columns="roleColumns" >
                <template #headerButton="{refresh}">
                    <RoleAdd @added="refresh"/>
                </template>
                <template #actions-cell="{row, refresh}">
                    <div class="flex flex-row justify-center items-center gap-2">
                        <RoleUpdate :role="row.original" @updated="refresh" />
                        <RoleDelete :role="row.original" @deleted="refresh" />
                    </div>
                </template>
                
            </ItemTable> 
        </template>
        <template #permissions>
            <ItemTable title="Дозволи" url="/api/v1/permissions/" :columns="permissionColumns" >
                <template #headerButton="{refresh}">
                    <PermissionAdd @added="refresh"/>
                </template>
                <template #actions-cell="{row, refresh}">
                    <div class="flex flex-row justify-center items-center gap-2">
                        <PermissionUpdate :permission="row.original" @updated="refresh" />
                        <PermissionDelete :permission="row.original" @deleted="refresh" />
                    </div>
                </template>
            </ItemTable>
        </template> 
    </UTabs>
</div>
</template>