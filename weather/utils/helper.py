def partial_by_index(list_object, index):
    def iter(l, result):
        if l == []:
            return result
        result.append(l[:index])
        return iter(l[index:], result)

    return iter(list_object, [])
